from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import AppSettings, Reminder, Task


def get_or_create_settings(db: Session) -> AppSettings:
    settings = db.query(AppSettings).first()
    if settings is None:
        settings = AppSettings(
            id=1,
            importance_low=10,
            importance_medium=25,
            importance_high=40,
            importance_critical=50,
            urgency_overdue=50,
            urgency_due_today=45,
            urgency_due_tomorrow=35,
            urgency_due_3_days=25,
            urgency_due_7_days=15,
            urgency_after_7_days=5,
            status_pending=10,
            status_in_progress=5,
            reminder_check_interval_minutes=15,
            upcoming_deadline_reminder_days=3,
            upcoming_deadline_reminder_enabled=True,
            overdue_reminder_enabled=True,
            dashboard_refresh_seconds=60,
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


def update_settings(db: Session, settings_data: dict) -> AppSettings:
    settings = get_or_create_settings(db)
    for key, value in settings_data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    db.commit()
    db.refresh(settings)
    return settings


def create_task(db: Session, task_input: dict) -> Task:
    if 'due_date' in task_input and task_input['due_date'] is not None and task_input['due_date'].tzinfo is None:
        task_input['due_date'] = task_input['due_date'].replace(tzinfo=timezone.utc)
    task = Task(**task_input)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db: Session, search: str | None = None, status: str | None = None, importance: str | None = None,
               overdue_only: bool = False, due_today: bool = False, due_this_week: bool = False,
               sort_by: str | None = None):
    query = db.query(Task)
    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))
    if status:
        query = query.filter(Task.status == status)
    if importance:
        query = query.filter(Task.importance == importance)
    now = datetime.now(timezone.utc)
    if overdue_only:
        query = query.filter(Task.status != 'Completed', Task.due_date < now)
    if due_today:
        query = query.filter(Task.status != 'Completed', func.date(Task.due_date) == func.date(now))
    if due_this_week:
        end_date = now + timedelta(days=7)
        query = query.filter(Task.status != 'Completed', Task.due_date >= now, Task.due_date <= end_date)
    if sort_by == 'deadline':
        query = query.order_by(Task.due_date.asc())
    elif sort_by == 'priority':
        query = query.order_by(Task.due_date.asc())
    else:
        query = query.order_by(Task.created_at.desc())
    return query.all()


def update_task(db: Session, task: Task, task_data: dict) -> Task:
    if 'due_date' in task_data and task_data['due_date'] is not None and task_data['due_date'].tzinfo is None:
        task_data['due_date'] = task_data['due_date'].replace(tzinfo=timezone.utc)
    for key, value in task_data.items():
        if value is not None:
            setattr(task, key, value)
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()


def complete_task(db: Session, task: Task) -> Task:
    task.status = 'Completed'
    task.completed_at = datetime.now(timezone.utc)
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task


def get_overdue_tasks(db: Session):
    now = datetime.now(timezone.utc)
    return db.query(Task).filter(Task.status != 'Completed', Task.due_date < now).order_by(Task.due_date.asc()).all()


def get_due_soon_tasks(db: Session, days_ahead: int = 7):
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days_ahead)
    return db.query(Task).filter(Task.status != 'Completed', Task.due_date >= now, Task.due_date <= end).order_by(Task.due_date.asc()).all()


def list_reminders(db: Session):
    return db.query(Reminder).order_by(Reminder.created_at.desc()).all()


def mark_reminder_read(db: Session, reminder_id: int) -> Reminder:
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if reminder is None:
        raise ValueError('Reminder not found')
    reminder.is_read = True
    db.commit()
    db.refresh(reminder)
    return reminder


def delete_reminder(db: Session, reminder_id: int) -> None:
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if reminder is not None:
        db.delete(reminder)
        db.commit()


def create_reminder(db: Session, task_id: int, reminder_type: str, message: str) -> Reminder:
    existing = db.query(Reminder).filter(
        Reminder.task_id == task_id,
        Reminder.reminder_type == reminder_type,
        Reminder.message == message,
    ).first()
    if existing:
        return existing
    reminder = Reminder(task_id=task_id, reminder_type=reminder_type, message=message, is_read=False)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def generate_reminders_for_task(db: Session, task: Task, settings) -> Iterable[Reminder]:
    if task.status == 'Completed':
        return []
    now = datetime.now(timezone.utc)
    due_date = task.due_date.replace(tzinfo=timezone.utc if task.due_date.tzinfo is None else task.due_date.tzinfo)
    delta_days = (due_date.date() - now.date()).days
    reminders = []

    if delta_days < 0 and settings.overdue_reminder_enabled:
        reminder = create_reminder(db, task.id, 'Overdue', f"Task '{task.title}' is overdue.")
        reminders.append(reminder)
    elif delta_days == 0 and settings.upcoming_deadline_reminder_enabled:
        reminder = create_reminder(db, task.id, 'Due today', f"Task '{task.title}' is due today.")
        reminders.append(reminder)
    elif 1 <= delta_days <= settings.upcoming_deadline_reminder_days and settings.upcoming_deadline_reminder_enabled:
        reminder_type = 'Upcoming deadline'
        reminder = create_reminder(db, task.id, reminder_type, f"Task '{task.title}' is due in {delta_days} day(s).")
        reminders.append(reminder)
    return reminders
