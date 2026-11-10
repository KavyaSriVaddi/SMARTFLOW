from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.database import SessionLocal
from app.models import Task


SAMPLE_TASKS = [
    {
        'title': 'Submit project report',
        'description': 'Finalize the capstone project report before submission.',
        'due_date': datetime.now(timezone.utc) + timedelta(days=1),
        'importance': 'Critical',
        'status': 'Pending',
        'estimated_duration': 4,
    },
    {
        'title': 'Prepare presentation',
        'description': 'Build slides and rehearse the presentation deck.',
        'due_date': datetime.now(timezone.utc) + timedelta(days=3),
        'importance': 'High',
        'status': 'In Progress',
        'estimated_duration': 5,
    },
    {
        'title': 'Organize study notes',
        'description': 'Sort and refine study materials for the next exam cycle.',
        'due_date': datetime.now(timezone.utc) + timedelta(days=7),
        'importance': 'Low',
        'status': 'Pending',
        'estimated_duration': 2,
    },
    {
        'title': 'Complete Python assignment',
        'description': 'Finish the Python coding assignment before class.',
        'due_date': datetime.now(timezone.utc),
        'importance': 'High',
        'status': 'Pending',
        'estimated_duration': 3,
    },
    {
        'title': 'Review completed project',
        'description': 'Audit the completed project and document final observations.',
        'due_date': datetime.now(timezone.utc) - timedelta(days=2),
        'importance': 'Medium',
        'status': 'Completed',
        'estimated_duration': 2,
        'completed_at': datetime.now(timezone.utc),
    },
]


def seed_sample_data():
    db = SessionLocal()
    try:
        for payload in SAMPLE_TASKS:
            existing = db.query(Task).filter(Task.title == payload['title']).first()
            if existing:
                continue
            task = Task(**payload)
            db.add(task)
        db.commit()
    finally:
        db.close()


def clear_sample_data():
    db = SessionLocal()
    try:
        for task in db.query(Task).filter(Task.title.in_([item['title'] for item in SAMPLE_TASKS])).all():
            db.delete(task)
        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    seed_sample_data()
    print('Sample data loaded into SMARTFLOW.')
