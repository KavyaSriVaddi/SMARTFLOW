from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import delete_reminder, list_reminders, mark_reminder_read
from app.database import get_db
from app.schemas import ReminderRead

router = APIRouter(prefix='/reminders', tags=['reminders'])


@router.get('', response_model=list[ReminderRead])
def get_all_reminders(db: Session = Depends(get_db)):
    return list_reminders(db)


@router.patch('/{reminder_id}/read', response_model=ReminderRead)
def read_reminder(reminder_id: int, db: Session = Depends(get_db)):
    try:
        reminder = mark_reminder_read(db, reminder_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return reminder


@router.delete('/{reminder_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder_endpoint(reminder_id: int, db: Session = Depends(get_db)):
    delete_reminder(db, reminder_id)
