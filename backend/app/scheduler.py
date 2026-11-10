from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from app.crud import generate_reminders_for_task, get_or_create_settings
from app.database import SessionLocal
from app.models import Task

scheduler = None


def check_and_create_reminders():
    db = SessionLocal()
    try:
        settings = get_or_create_settings(db)
        tasks = db.query(Task).filter(Task.status != 'Completed').all()
        for task in tasks:
            generate_reminders_for_task(db, task, settings)
    finally:
        db.close()


def start_scheduler():
    global scheduler
    if scheduler is not None:
        return scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_create_reminders, 'interval', minutes=15, id='smartflow_deadline_checks', replace_existing=True)
    scheduler.start()
    return scheduler


def shutdown_scheduler():
    global scheduler
    if scheduler is not None:
        scheduler.shutdown()
        scheduler = None
