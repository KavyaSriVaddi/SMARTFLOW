from __future__ import annotations

from datetime import datetime, timezone


def get_deadline_flag(task, now=None):
    task_now = now or datetime.now(timezone.utc)
    if task_now.tzinfo is None:
        task_now = task_now.replace(tzinfo=timezone.utc)
    due_date = task.due_date
    if due_date.tzinfo is None:
        due_date = due_date.replace(tzinfo=timezone.utc)
    if task.status == 'Completed':
        return {'label': 'Completed', 'color': 'green', 'is_overdue': False}
    delta = due_date - task_now
    days_left = delta.days
    if days_left < 0:
        return {'label': 'Overdue', 'color': 'red', 'is_overdue': True}
    if days_left == 0:
        return {'label': 'Due today', 'color': 'orange', 'is_overdue': False}
    if days_left == 1:
        return {'label': 'Due tomorrow', 'color': 'yellow', 'is_overdue': False}
    if days_left <= 3:
        return {'label': 'Due soon', 'color': 'yellow', 'is_overdue': False}
    return {'label': 'Upcoming', 'color': 'blue', 'is_overdue': False}
