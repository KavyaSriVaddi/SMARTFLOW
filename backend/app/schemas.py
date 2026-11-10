from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator

VALID_IMPORTANCES = {'Low', 'Medium', 'High', 'Critical'}
VALID_STATUSES = {'Pending', 'In Progress', 'Completed'}


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = None
    due_date: datetime
    importance: str = 'Medium'
    status: str = 'Pending'
    estimated_duration: int | None = None
    actual_duration: int | None = None

    @field_validator('due_date')
    @classmethod
    def normalize_due_date(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @field_validator('importance')
    @classmethod
    def validate_importance(cls, value: str) -> str:
        value = value.strip()
        if value not in VALID_IMPORTANCES:
            raise ValueError('Importance must be one of: Low, Medium, High, Critical')
        return value

    @field_validator('status')
    @classmethod
    def validate_status(cls, value: str) -> str:
        value = value.strip()
        if value not in VALID_STATUSES:
            raise ValueError('Status must be one of: Pending, In Progress, Completed')
        return value


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    importance: str | None = None
    status: str | None = None
    estimated_duration: int | None = None
    actual_duration: int | None = None

    @field_validator('due_date')
    @classmethod
    def normalize_due_date(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @field_validator('importance')
    @classmethod
    def validate_importance(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if value not in VALID_IMPORTANCES:
            raise ValueError('Importance must be one of: Low, Medium, High, Critical')
        return value

    @field_validator('status')
    @classmethod
    def validate_status(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if value not in VALID_STATUSES:
            raise ValueError('Status must be one of: Pending, In Progress, Completed')
        return value


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    priority_score: int | None = None
    priority_category: str | None = None
    priority_explanation: str | None = None
    suggested_rank: int | None = None


class ReminderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    reminder_type: str
    message: str
    created_at: datetime
    is_read: bool


class SettingsUpdate(BaseModel):
    importance_low: int = 10
    importance_medium: int = 25
    importance_high: int = 40
    importance_critical: int = 50
    urgency_overdue: int = 50
    urgency_due_today: int = 45
    urgency_due_tomorrow: int = 35
    urgency_due_3_days: int = 25
    urgency_due_7_days: int = 15
    urgency_after_7_days: int = 5
    status_pending: int = 10
    status_in_progress: int = 5
    reminder_check_interval_minutes: int = 15
    upcoming_deadline_reminder_days: int = 3
    upcoming_deadline_reminder_enabled: bool = True
    overdue_reminder_enabled: bool = True
    dashboard_refresh_seconds: int = 60


class SettingsRead(SettingsUpdate):
    id: int
