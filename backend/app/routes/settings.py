from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import get_or_create_settings, update_settings
from app.database import get_db
from app.schemas import SettingsRead, SettingsUpdate

router = APIRouter(prefix='/settings', tags=['settings'])


@router.get('', response_model=SettingsRead)
def get_settings(db: Session = Depends(get_db)):
    settings = get_or_create_settings(db)
    return SettingsRead.model_validate(settings)


@router.put('', response_model=SettingsRead)
def update_settings_endpoint(settings_data: SettingsUpdate, db: Session = Depends(get_db)):
    settings = update_settings(db, settings_data.model_dump())
    return SettingsRead.model_validate(settings)
