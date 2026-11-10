from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from app.models import Task


def calculate_summary(db):
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == 'Completed').count()
    pending_tasks = db.query(Task).filter(Task.status == 'Pending').count()
    in_progress_tasks = db.query(Task).filter(Task.status == 'In Progress').count()
    overdue_tasks = db.query(Task).filter(Task.status != 'Completed', Task.due_date < datetime.now(timezone.utc)).count()
    completion_rate = round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0

    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': completion_rate,
    }


def calculate_status_distribution(db):
    tasks = db.query(Task).all()
    if not tasks:
        return []
    df = pd.DataFrame([{'status': task.status} for task in tasks])
    grouped = df.groupby('status').size().reset_index(name='value')
    return [{'name': row['status'], 'value': int(row['value'])} for _, row in grouped.iterrows()]


def calculate_importance_distribution(db):
    tasks = db.query(Task).all()
    if not tasks:
        return []
    df = pd.DataFrame([{'importance': task.importance} for task in tasks])
    for level in ['Low', 'Medium', 'High', 'Critical']:
        if level not in df['importance'].values:
            df = pd.concat([df, pd.DataFrame([{'importance': level}])], ignore_index=True)
    grouped = df.groupby('importance').size().reset_index(name='value')
    grouped = grouped[grouped['importance'].isin(['Low', 'Medium', 'High', 'Critical'])].sort_values('importance')
    return [{'name': row['importance'], 'value': int(row['value'])} for _, row in grouped.iterrows()]


def calculate_completion_trend(db):
    tasks = db.query(Task).filter(Task.status == 'Completed').all()
    if not tasks:
        return []
    df = pd.DataFrame([{ 'completed_date': task.completed_at.date().isoformat() if task.completed_at else None} for task in tasks])
    df = df.dropna()
    if df.empty:
        return []
    grouped = df.groupby('completed_date').size().reset_index(name='completed')
    return [{'date': row['completed_date'], 'completed': int(row['completed'])} for _, row in grouped.iterrows()]


def calculate_weekly_productivity(db):
    tasks = db.query(Task).filter(Task.status == 'Completed').all()
    if not tasks:
        return []
    rows = [{'completed_week': task.completed_at.strftime('%Y-W%U') if task.completed_at else None} for task in tasks]
    df = pd.DataFrame(rows).dropna()
    if df.empty:
        return []
    grouped = df.groupby('completed_week').size().reset_index(name='completed')
    return [{'week': row['completed_week'], 'completed': int(row['completed'])} for _, row in grouped.iterrows()]


def calculate_overdue_analysis(db):
    tasks = db.query(Task).filter(Task.status != 'Completed', Task.due_date < datetime.now(timezone.utc)).all()
    if not tasks:
        return []
    df = pd.DataFrame([{'importance': task.importance, 'title': task.title} for task in tasks])
    grouped = df.groupby('importance').size().reset_index(name='count')
    return [{'name': row['importance'], 'count': int(row['count'])} for _, row in grouped.iterrows()]
