from datetime import datetime, timedelta, timezone

from app.services.priority_engine import calculate_priority


class DummyTask:
    def __init__(self, importance, status, due_date):
        self.importance = importance
        self.status = status
        self.due_date = due_date


def test_low_importance_task():
    task = DummyTask('Low', 'Pending', datetime.now(timezone.utc) + timedelta(days=5))
    result = calculate_priority(task)
    assert result['score'] >= 0
    assert result['category'] in {'Low', 'Medium'}


def test_high_importance_task():
    task = DummyTask('High', 'Pending', datetime.now(timezone.utc) + timedelta(days=2))
    result = calculate_priority(task)
    assert result['score'] > 40


def test_critical_importance_task():
    task = DummyTask('Critical', 'Pending', datetime.now(timezone.utc) + timedelta(days=1))
    result = calculate_priority(task)
    assert result['category'] in {'Critical', 'High'}


def test_overdue_task():
    task = DummyTask('Critical', 'Pending', datetime.now(timezone.utc) - timedelta(days=2))
    result = calculate_priority(task)
    assert result['score'] >= 70


def test_completed_task_excluded():
    task = DummyTask('High', 'Completed', datetime.now(timezone.utc) + timedelta(days=2))
    result = calculate_priority(task)
    assert result['score'] == 0


def test_priority_ordering():
    tasks = [
        DummyTask('Low', 'Pending', datetime.now(timezone.utc) + timedelta(days=8)),
        DummyTask('Critical', 'Pending', datetime.now(timezone.utc) + timedelta(days=1)),
        DummyTask('High', 'In Progress', datetime.now(timezone.utc) + timedelta(days=2)),
    ]
    ordered = sorted(tasks, key=lambda item: calculate_priority(item)['score'], reverse=True)
    assert ordered[0].importance == 'Critical'
