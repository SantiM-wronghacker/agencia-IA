"""Tests for the SQLite TaskRepository – CRUD + persistence across restarts."""

import os
import sys
import uuid
from datetime import datetime, timezone

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.agencia.api.dashboard.models import TaskSchema, TaskStatus
from src.agencia.api.dashboard.repository import TaskRepository


def _make_task(**overrides) -> TaskSchema:
    now = datetime.now(timezone.utc)
    defaults = {
        "id": str(uuid.uuid4()),
        "name": "test-task",
        "status": TaskStatus.PENDING,
        "description": "desc",
        "created_at": now,
        "updated_at": now,
    }
    defaults.update(overrides)
    return TaskSchema(**defaults)


@pytest.fixture()
def repo(tmp_path):
    return TaskRepository(db_path=str(tmp_path / "test.db"))


# ---- Create / Get ----


def test_create_and_get(repo):
    task = _make_task(name="Alpha")
    repo.create(task)
    fetched = repo.get(task.id)
    assert fetched is not None
    assert fetched.name == "Alpha"
    assert fetched.status == TaskStatus.PENDING


def test_get_missing_returns_none(repo):
    assert repo.get("nonexistent") is None


# ---- List ----


def test_list_all(repo):
    repo.create(_make_task(name="A"))
    repo.create(_make_task(name="B"))
    assert len(repo.list_all()) == 2


def test_list_filter_by_status(repo):
    repo.create(_make_task(name="P", status=TaskStatus.PENDING))
    repo.create(_make_task(name="R", status=TaskStatus.RUNNING))
    result = repo.list_all(status_filter="running")
    assert len(result) == 1
    assert result[0].name == "R"


def test_list_search(repo):
    repo.create(_make_task(name="Deploy API"))
    repo.create(_make_task(name="Train model"))
    result = repo.list_all(search="deploy")
    assert len(result) == 1
    assert "Deploy" in result[0].name


# ---- Update ----


def test_update(repo):
    task = _make_task(name="Before")
    repo.create(task)
    task.name = "After"
    task.status = TaskStatus.RUNNING
    repo.update(task)
    fetched = repo.get(task.id)
    assert fetched is not None
    assert fetched.name == "After"
    assert fetched.status == TaskStatus.RUNNING


# ---- Delete ----


def test_delete(repo):
    task = _make_task()
    repo.create(task)
    assert repo.delete(task.id) is True
    assert repo.get(task.id) is None


def test_delete_missing(repo):
    assert repo.delete("nope") is False


# ---- Metrics ----


def test_metrics_empty(repo):
    m = repo.metrics()
    assert m["total_tasks"] == 0
    assert m["success_rate"] == 0.0


def test_metrics_counts(repo):
    repo.create(_make_task(status=TaskStatus.PENDING))
    repo.create(_make_task(status=TaskStatus.RUNNING))
    repo.create(_make_task(status=TaskStatus.COMPLETED))
    repo.create(_make_task(status=TaskStatus.FAILED))
    m = repo.metrics()
    assert m["total_tasks"] == 4
    assert m["pending"] == 1
    assert m["running"] == 1
    assert m["completed"] == 1
    assert m["failed"] == 1
    assert m["success_rate"] == 25.0


# ---- Persistence across restarts ----


def test_data_survives_restart(tmp_path):
    """Simulate app restart: create repo, add task, destroy repo, create new one."""
    db_path = str(tmp_path / "persist.db")
    repo1 = TaskRepository(db_path=db_path)
    task = _make_task(name="Persistent")
    repo1.create(task)

    # "restart" – new repository instance, same DB file
    repo2 = TaskRepository(db_path=db_path)
    fetched = repo2.get(task.id)
    assert fetched is not None
    assert fetched.name == "Persistent"
