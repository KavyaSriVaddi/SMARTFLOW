# SMARTFLOW Architecture

SMARTFLOW follows a layered architecture designed for a small, maintainable Python full-stack application.

## Layered Overview

### 1. Frontend Layer

- Built with Streamlit
- Provides dashboard pages, task forms, notification views, and settings panels
- Calls backend REST endpoints using HTTPX
- Displays metrics, charts, and task summaries generated from real database records

### 2. Backend Layer

- Built with FastAPI
- Exposes REST endpoints for tasks, analytics, reminders, and system settings
- Validates request payloads with Pydantic schemas
- Performs database operations through SQLAlchemy models and CRUD helpers

### 3. Data Layer

- SQLite database with SQLAlchemy ORM
- Stores task records, reminder records, and settings
- Persists user-created tasks across application restarts

### 4. Service Layer

- Smart priority engine computes scoring and recommendation explanations
- Deadline monitor identifies overdue and upcoming tasks
- Analytics service produces summary, productivity, and distribution metrics
- Scheduler service triggers reminder creation and tracking

## Core Workflow

1. The user interacts with the Streamlit dashboard.
2. The frontend sends requests to the FastAPI backend.
3. FastAPI validates the request and calls the relevant CRUD or service function.
4. SQLAlchemy reads or writes SQLite records.
5. The backend returns structured JSON responses back to the frontend.
6. The dashboard updates task lists, metrics, and reminder views in real time.

## Main Modules

- backend/app/main.py: application startup, router registration, and health checks
- backend/app/models.py: SQLAlchemy data models
- backend/app/schemas.py: request and response validation models
- backend/app/crud.py: database operations and data access logic
- backend/app/services/priority_engine.py: scoring and ranking logic
- backend/app/services/deadline_monitor.py: task urgency checks
- backend/app/services/analytics_service.py: summary and chart metrics
- backend/app/scheduler.py: reminder scheduling lifecycle
- frontend/app.py: Streamlit entry point and navigation
- frontend/components/*: dashboard, task form, table, charts, and sidebar UI modules

## Design Principles

- Preserve the existing architecture and avoid unnecessary rewrites
- Keep analytics and priorities based on actual records instead of hardcoded values
- Favor rule-based transparency over opaque prediction logic
- Support clean API-based integration between frontend and backend
- Keep the app accessible for local development and academic demonstration

## Request Flow Example

A task is created through the Streamlit form:

1. User enters title, due date, importance, and status.
2. Streamlit sends a POST request to /api/tasks.
3. FastAPI validates the payload.
4. SQLAlchemy inserts the task into SQLite.
5. The backend returns the task with computed priority metadata.
6. The dashboard refreshes the task list and metrics.
