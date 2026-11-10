from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import complete_task, create_task, delete_task, get_or_create_settings, get_task, list_tasks, update_task
from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate
from app.services.priority_engine import calculate_priority

router = APIRouter(prefix='/tasks', tags=['tasks'])


def build_task_response(task: Task, settings):
    priority = calculate_priority(task, settings)
    task_response = TaskRead.model_validate(task)
    task_response.priority_score = priority['score']
    task_response.priority_category = priority['category']
    task_response.priority_explanation = priority['explanation']
    task_response.suggested_rank = priority['suggested_rank']
    return task_response


@router.post('', response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(task_data: TaskCreate, db: Session = Depends(get_db)):
    settings = get_or_create_settings(db)
    task = create_task(db, task_data.model_dump())
    return build_task_response(task, settings)


@router.get('', response_model=list[TaskRead])
def read_tasks(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    importance: Optional[str] = Query(None),
    overdue_only: bool = Query(False),
    due_today: bool = Query(False),
    due_this_week: bool = Query(False),
    sort_by: Optional[str] = Query(None),
):
    settings = get_or_create_settings(db)
    tasks = list_tasks(db, search=search, status=status, importance=importance, overdue_only=overdue_only,
                      due_today=due_today, due_this_week=due_this_week, sort_by=sort_by)
    return [build_task_response(task, settings) for task in tasks]


@router.get('/{task_id}', response_model=TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db)):
    settings = get_or_create_settings(db)
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return build_task_response(task, settings)


@router.put('/{task_id}', response_model=TaskRead)
def update_task_endpoint(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    settings = get_or_create_settings(db)
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    update = task_data.model_dump(exclude_unset=True)
    task = update_task(db, task, update)
    return build_task_response(task, settings)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    delete_task(db, task)


@router.patch('/{task_id}/complete', response_model=TaskRead)
def complete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    settings = get_or_create_settings(db)
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    task = complete_task(db, task)
    return build_task_response(task, settings)


@router.get('/prioritized', response_model=list[TaskRead])
def prioritized_tasks(db: Session = Depends(get_db)):
    settings = get_or_create_settings(db)
    tasks = [task for task in db.query(Task).all() if task.status != 'Completed']
    ranked_tasks = sorted(tasks, key=lambda item: calculate_priority(item, settings)['score'], reverse=True)
    responses = []
    for index, task in enumerate(ranked_tasks, start=1):
        response = build_task_response(task, settings)
        response.suggested_rank = index
        responses.append(response)
    return responses


@router.get('/overdue', response_model=list[TaskRead])
def overdue_tasks(db: Session = Depends(get_db)):
    settings = get_or_create_settings(db)
    tasks = db.query(Task).filter(Task.status != 'Completed', Task.due_date < datetime.now(timezone.utc)).order_by(Task.due_date.asc()).all()
    return [build_task_response(task, settings) for task in tasks]


@router.get('/due-soon', response_model=list[TaskRead])
def due_soon_tasks(db: Session = Depends(get_db)):
    settings = get_or_create_settings(db)
    from datetime import datetime, timedelta, timezone
    end = datetime.now(timezone.utc) + timedelta(days=7)
    tasks = db.query(Task).filter(Task.status != 'Completed', Task.due_date >= datetime.now(timezone.utc), Task.due_date <= end).order_by(Task.due_date.asc()).all()
    return [build_task_response(task, settings) for task in tasks]
