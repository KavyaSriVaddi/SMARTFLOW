from __future__ import annotations

from datetime import datetime, timezone

DEFAULT_PRIORITY_WEIGHTS = {
    'Low': 10,
    'Medium': 25,
    'High': 40,
    'Critical': 50,
    'Overdue': 50,
    'Due today': 45,
    'Due tomorrow': 35,
    'Due within 3 days': 25,
    'Due within 7 days': 15,
    'Due after 7 days': 5,
    'Pending': 10,
    'In Progress': 5,
}


def get_weight_mapping(settings=None):
    if settings is None:
        return {
            'Low': 10,
            'Medium': 25,
            'High': 40,
            'Critical': 50,
            'Overdue': 50,
            'Due today': 45,
            'Due tomorrow': 35,
            'Due within 3 days': 25,
            'Due within 7 days': 15,
            'Due after 7 days': 5,
            'Pending': 10,
            'In Progress': 5,
        }
    return {
        'Low': settings.importance_low,
        'Medium': settings.importance_medium,
        'High': settings.importance_high,
        'Critical': settings.importance_critical,
        'Overdue': settings.urgency_overdue,
        'Due today': settings.urgency_due_today,
        'Due tomorrow': settings.urgency_due_tomorrow,
        'Due within 3 days': settings.urgency_due_3_days,
        'Due within 7 days': settings.urgency_due_7_days,
        'Due after 7 days': settings.urgency_after_7_days,
        'Pending': settings.status_pending,
        'In Progress': settings.status_in_progress,
    }


def calculate_priority(task, settings=None, now=None):
    weights = get_weight_mapping(settings)
    task_now = now or datetime.now(timezone.utc)
    if task_now.tzinfo is None:
        task_now = task_now.replace(tzinfo=timezone.utc)
    due_date = task.due_date
    if due_date.tzinfo is None:
        due_date = due_date.replace(tzinfo=timezone.utc)

    if task.status == 'Completed':
        return {
            'score': 0,
            'category': 'Low',
            'explanation': 'Completed tasks are excluded from active prioritization.',
            'suggested_rank': 0,
        }

    importance_weight = weights.get(task.importance, weights['Medium'])
    urgency_weight = 0
    days_until = (due_date.date() - task_now.date()).days

    if due_date < task_now:
        urgency_weight = weights['Overdue']
        urgency_label = 'overdue'
    elif days_until == 0:
        urgency_weight = weights['Due today']
        urgency_label = 'due today'
    elif days_until == 1:
        urgency_weight = weights['Due tomorrow']
        urgency_label = 'due tomorrow'
    elif days_until <= 3:
        urgency_weight = weights['Due within 3 days']
        urgency_label = 'due within 3 days'
    elif days_until <= 7:
        urgency_weight = weights['Due within 7 days']
        urgency_label = 'due within 7 days'
    else:
        urgency_weight = weights['Due after 7 days']
        urgency_label = 'due later'

    status_weight = weights.get(task.status, weights['Pending'])
    score = max(0, min(100, importance_weight + urgency_weight + status_weight))

    if score >= 80:
        category = 'Critical'
    elif score >= 60:
        category = 'High'
    elif score >= 35:
        category = 'Medium'
    else:
        category = 'Low'

    explanation = f'{category} priority because the task is marked {task.importance} and is {urgency_label}.'
    return {
        'score': int(score),
        'category': category,
        'explanation': explanation,
        'suggested_rank': 0,
    }
