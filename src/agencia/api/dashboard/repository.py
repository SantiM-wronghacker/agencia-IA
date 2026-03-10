"""
SQLite-backed task repository for persistent storage.
"""
from __future__ import annotations

import json
import logging
import os
import sqlite3
from datetime import datetime, timezone
from typing import Optional

from .models import TaskSchema, TaskStatus

logger = logging.getLogger(__name__)

_DB_PATH = os.environ.get("DASHBOARD_DB_PATH", os.path.join("data", "tasks.db"))


def _ensure_dir(path: str) -> None:
    """Create parent directory for the database file if it doesn't exist."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def _get_db_path() -> str:
    """Return the resolved database path."""
    return _DB_PATH


def set_db_path(path: str) -> None:
    """Override the database path (useful for testing)."""
    global _DB_PATH
    _DB_PATH = path


class TaskRepository:
    """SQLite-backed task storage with auto-create table."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or _get_db_path()
        _ensure_dir(self.db_path)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # WAL mode improves concurrent read performance and reduces lock contention
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self) -> None:
        """Create the tasks table if it doesn't exist."""
        conn = self._get_conn()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    description TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    result TEXT,
                    logs TEXT NOT NULL DEFAULT '[]'
                )
            """)
            conn.commit()
            logger.info("SQLite task repository initialized at %s", self.db_path)
        finally:
            conn.close()

    def create(self, task: TaskSchema) -> TaskSchema:
        """Insert a new task."""
        conn = self._get_conn()
        try:
            conn.execute(
                """INSERT INTO tasks (id, name, status, description, created_at, updated_at, result, logs)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    task.id,
                    task.name,
                    task.status.value,
                    task.description,
                    task.created_at.isoformat(),
                    task.updated_at.isoformat(),
                    json.dumps(task.result) if task.result is not None else None,
                    json.dumps(task.logs),
                ),
            )
            conn.commit()
            return task
        finally:
            conn.close()

    def get(self, task_id: str) -> Optional[TaskSchema]:
        """Get a task by ID."""
        conn = self._get_conn()
        try:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if row is None:
                return None
            return self._row_to_task(row)
        finally:
            conn.close()

    def list_tasks(
        self,
        status_filter: Optional[TaskStatus] = None,
        search: Optional[str] = None,
    ) -> list[TaskSchema]:
        """List tasks with optional filters."""
        conn = self._get_conn()
        try:
            query = "SELECT * FROM tasks WHERE 1=1"
            params: list[str] = []

            if status_filter is not None:
                query += " AND status = ?"
                params.append(status_filter.value)

            if search:
                query += " AND (LOWER(name) LIKE ? OR LOWER(COALESCE(description, '')) LIKE ?)"
                like = f"%{search.lower()}%"
                params.extend([like, like])

            query += " ORDER BY created_at DESC"

            rows = conn.execute(query, params).fetchall()
            return [self._row_to_task(r) for r in rows]
        finally:
            conn.close()

    def update(self, task: TaskSchema) -> TaskSchema:
        """Update an existing task."""
        conn = self._get_conn()
        try:
            conn.execute(
                """UPDATE tasks SET name=?, status=?, description=?, updated_at=?, result=?, logs=?
                   WHERE id=?""",
                (
                    task.name,
                    task.status.value,
                    task.description,
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
            conn.commit()
            return task
        finally:
            conn.close()

    def count_by_status(self) -> dict[str, int]:
        """Get task counts grouped by status."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT status, COUNT(*) as cnt FROM tasks GROUP BY status"
            ).fetchall()
            return {row["status"]: row["cnt"] for row in rows}
        finally:
            conn.close()

    def total_count(self) -> int:
        """Get total number of tasks."""
        conn = self._get_conn()
        try:
            row = conn.execute("SELECT COUNT(*) as cnt FROM tasks").fetchone()
            return row["cnt"] if row else 0
        finally:
            conn.close()

    def clear(self) -> None:
        """Delete all tasks (for testing)."""
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM tasks")
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> TaskSchema:
        """Convert a database row to a TaskSchema."""
        result_raw = row["result"]
        result = json.loads(result_raw) if result_raw is not None else None
        logs = json.loads(row["logs"]) if row["logs"] else []

        return TaskSchema(
            id=row["id"],
            name=row["name"],
            status=TaskStatus(row["status"]),
            description=row["description"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            result=result,
            logs=logs,
        )
