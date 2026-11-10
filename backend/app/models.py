from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=False)
    importance = Column(String(20), nullable=False, default='Medium')
    status = Column(String(20), nullable=False, default='Pending')
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    estimated_duration = Column(Integer, nullable=True)
    actual_duration = Column(Integer, nullable=True)
    reminders = relationship('Reminder', back_populates='task', cascade='all, delete-orphan')


class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    reminder_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    task = relationship('Task', back_populates='reminders')


class AppSettings(Base):
    __tablename__ = 'app_settings'

    id = Column(Integer, primary_key=True, default=1)
    importance_low = Column(Integer, default=10, nullable=False)
    importance_medium = Column(Integer, default=25, nullable=False)
    importance_high = Column(Integer, default=40, nullable=False)
    importance_critical = Column(Integer, default=50, nullable=False)
    urgency_overdue = Column(Integer, default=50, nullable=False)
    urgency_due_today = Column(Integer, default=45, nullable=False)
    urgency_due_tomorrow = Column(Integer, default=35, nullable=False)
    urgency_due_3_days = Column(Integer, default=25, nullable=False)
    urgency_due_7_days = Column(Integer, default=15, nullable=False)
    urgency_after_7_days = Column(Integer, default=5, nullable=False)
    status_pending = Column(Integer, default=10, nullable=False)
    status_in_progress = Column(Integer, default=5, nullable=False)
    reminder_check_interval_minutes = Column(Integer, default=15, nullable=False)
    upcoming_deadline_reminder_days = Column(Integer, default=3, nullable=False)
    upcoming_deadline_reminder_enabled = Column(Boolean, default=True, nullable=False)
    overdue_reminder_enabled = Column(Boolean, default=True, nullable=False)
    dashboard_refresh_seconds = Column(Integer, default=60, nullable=False)
