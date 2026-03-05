"""SQLite-backed task repository for the Dashboard API."""

from __future__ import annotations

import json
import os
import sqlite3
import threading
from datetime import datetime
from pathlib import Path

from .models import TaskSchema, TaskStatus

_DEFAULT_DB_PATH = "./data/dashboard.db"


class TaskRepository:
    """Thread-safe SQLite repository for tasks."""

    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path or os.getenv("DASHBOARD_DB_PATH", _DEFAULT_DB_PATH)
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_table()

    def _init_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                result TEXT,
                logs TEXT
            )
            """
        )
        self._conn.commit()

    # -- helpers ----------------------------------------------------------

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> TaskSchema:
        return TaskSchema(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            status=TaskStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            result=json.loads(row["result"]) if row["result"] is not None else None,
            logs=json.loads(row["logs"]) if row["logs"] is not None else [],
        )

    # -- public API -------------------------------------------------------

    def create(self, task: TaskSchema) -> TaskSchema:
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO tasks (id, name, description, status, created_at, updated_at, result, logs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task.id,
                    task.name,
                    task.description,
                    task.status.value,
                    task.created_at.isoformat(),
                    task.updated_at.isoformat(),
                    json.dumps(task.result) if task.result is not None else None,
                    json.dumps(task.logs),
                ),
            )
            self._conn.commit()
        return task

    def get(self, task_id: str) -> TaskSchema | None:
        with self._lock:
            cur = self._conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cur.fetchone()
        if row is None:
            return None
        return self._row_to_task(row)

    def list_all(
        self,
        status_filter: str | None = None,
        search: str | None = None,
    ) -> list[TaskSchema]:
        query = "SELECT * FROM tasks"
        params: list[str] = []
        clauses: list[str] = []

        if status_filter:
            clauses.append("status = ?")
            params.append(status_filter)
        if search:
            clauses.append("(name LIKE ? OR description LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        query += " ORDER BY created_at DESC"

        with self._lock:
            cur = self._conn.execute(query, params)
            rows = cur.fetchall()
        return [self._row_to_task(row) for row in rows]

    def update(self, task: TaskSchema) -> TaskSchema:
        with self._lock:
            self._conn.execute(
                """
                UPDATE tasks
                   SET name = ?, description = ?, status = ?,
                       updated_at = ?, result = ?, logs = ?
                 WHERE id = ?
                """,
                (
                    task.name,
                    task.description,
                    task.status.value,
                    task.updated_at.isoformat(),
                    json.dumps(task.result) if task.result is not None else None,
                    json.dumps(task.logs),
                    task.id,
                ),
            )
            self._conn.commit()
        return task

    def delete(self, task_id: str) -> bool:
        with self._lock:
            cur = self._conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self._conn.commit()
        return cur.rowcount > 0

    def metrics(self) -> dict:
        with self._lock:
            cur = self._conn.execute(
                """
                SELECT
                    COUNT(*)                                        AS total_tasks,
                    SUM(CASE WHEN status = ? THEN 1 ELSE 0 END)    AS completed,
                    SUM(CASE WHEN status = ? THEN 1 ELSE 0 END)    AS failed,
                    SUM(CASE WHEN status = ? THEN 1 ELSE 0 END)    AS pending,
                    SUM(CASE WHEN status = ? THEN 1 ELSE 0 END)    AS running
                FROM tasks
                """,
                (
                    TaskStatus.COMPLETED.value,
                    TaskStatus.FAILED.value,
                    TaskStatus.PENDING.value,
                    TaskStatus.RUNNING.value,
                ),
            )
            row = cur.fetchone()
        total = row["total_tasks"] or 0
        completed = row["completed"] or 0
        return {
            "total_tasks": total,
            "completed": completed,
            "failed": row["failed"] or 0,
            "pending": row["pending"] or 0,
            "running": row["running"] or 0,
            "success_rate": round((completed / total) * 100.0, 2) if total else 0.0,
        }
