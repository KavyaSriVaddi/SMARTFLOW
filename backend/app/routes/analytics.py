from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.analytics_service import (
    calculate_completion_trend,
    calculate_importance_distribution,
    calculate_overdue_analysis,
    calculate_status_distribution,
    calculate_summary,
    calculate_weekly_productivity,
)

router = APIRouter(prefix='/analytics', tags=['analytics'])


@router.get('/summary')
def summary(db: Session = Depends(get_db)):
    return calculate_summary(db)


@router.get('/status-distribution')
def status_distribution(db: Session = Depends(get_db)):
    return calculate_status_distribution(db)


@router.get('/importance-distribution')
def importance_distribution(db: Session = Depends(get_db)):
    return calculate_importance_distribution(db)


@router.get('/completion-trend')
def completion_trend(db: Session = Depends(get_db)):
    return calculate_completion_trend(db)


@router.get('/weekly-productivity')
def weekly_productivity(db: Session = Depends(get_db)):
    return calculate_weekly_productivity(db)


@router.get('/overdue-analysis')
def overdue_analysis(db: Session = Depends(get_db)):
    return calculate_overdue_analysis(db)
