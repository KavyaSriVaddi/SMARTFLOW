from datetime import datetime, timedelta, timezone

from app.crud import create_reminder, generate_reminders_for_task, get_or_create_settings
from app.database import SessionLocal
from app.models import Task


def test_upcoming_deadline_detection():
    db = SessionLocal()
    settings = get_or_create_settings(db)
    task = Task(
        title='Prepare interview',
        description='Practice presentation',
        due_date=datetime.now(timezone.utc) + timedelta(days=2),
        importance='High',
        status='Pending',
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    reminders = generate_reminders_for_task(db, task, settings)
    assert any(reminder.reminder_type == 'Upcoming deadline' for reminder in reminders)
    db.delete(task)
    db.commit()
    db.close()


def test_duplicate_reminder_prevention():
    db = SessionLocal()
    task = Task(
        title='Draft notes',
        description='Review notes',
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        importance='Medium',
        status='Pending',
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    first = create_reminder(db, task.id, 'Upcoming deadline', "Task 'Draft notes' is due in 1 day(s).")
    second = create_reminder(db, task.id, 'Upcoming deadline', "Task 'Draft notes' is due in 1 day(s).")
    assert first.id == second.id
    db.delete(task)
    db.commit()
    db.close()
