# SMARTFLOW

SMARTFLOW is an intelligent task management and workload optimization system developed with Python, FastAPI, SQLite, SQLAlchemy, Streamlit, Pandas, Matplotlib, and APScheduler.

## Overview

The project helps students and professionals organize work, prioritize important tasks, monitor deadlines, and review productivity trends through a rule-based smart priority engine and a live dashboard. The system is designed to remain lightweight and easy to run locally while still supporting API-driven workflows and dashboard analytics.

## Core Features

- Task creation, update, completion, and deletion
- Importance and status tracking
- Smart task ranking based on urgency, importance, and deadline pressure
- Deadline monitoring for overdue and due-soon tasks
- Reminder generation and in-app notification tracking
- Dashboard metrics for task health and productivity
- Settings management for priority weighting and reminder behavior
- SQLite persistence with SQLAlchemy models
- Full backend API with Swagger/OpenAPI documentation
- Automated pytest coverage for critical flows

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Pydantic, SQLite, Uvicorn
- Frontend: Streamlit
- Analytics: Pandas, Matplotlib
- Scheduling: APScheduler
- Testing: Pytest, FastAPI TestClient

## Project Structure

```text
SMARTFLOW/
├── backend/
│   ├── app/
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── sample_data.py
│   │   ├── schemas.py
│   │   ├── scheduler.py
│   │   ├── routes/
│   │   └── services/
│   └── tests/
├── frontend/
│   ├── app.py
│   ├── components/
│   └── styles/
├── docs/
│   ├── api_documentation.md
│   └── architecture.md
├── README.md
├── conftest.py
├── requirements.txt
├── run_backend.bat
├── run_frontend.bat
├── run_project.bat
└── .env.example
```

## Installation

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Verify the environment is ready.

## Run the Backend

From the project root:

```bash
cd backend
set PYTHONPATH=.
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Or on Windows PowerShell:

```powershell
Set-Location "C:\Users\Kavya Sri\OneDrive\Attachments\Desktop\SMARTFLOW\backend"
$env:PYTHONPATH = "."
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Run the Frontend

```bash
streamlit run frontend/app.py
```

## Windows Launcher Scripts

The project includes:

- run_backend.bat
- run_frontend.bat
- run_project.bat

These can be used to start the backend and frontend in a local Windows development environment.

## API and Swagger

Once the backend is running, Swagger UI is available here:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

The application also exposes a health check endpoint:

- GET /health

## Database Design

SMARTFLOW uses SQLite as its persistence layer with SQLAlchemy ORM models for:

- tasks
- reminders
- settings

Data is stored in the backend database folder and is retained across app restarts. The application avoids destructive resets during normal usage and preserves existing user-created records when possible.

## Smart Priority Algorithm

The priority engine combines the following logic:

- Importance weight based on task category (Low, Medium, High, Critical)
- Deadline urgency, including overdue, due today, due soon, and after-deadline logic
- Status adjustment for pending or active work
- Score normalization used to rank tasks in a transparent and explainable way

Each task receives:

- priority_score
- priority_category
- priority_explanation
- suggested_rank

These values are returned with task reads and priority ranking endpoints so the recommendation is understandable to the user.

## Deadline and Reminder Behavior

SMARTFLOW monitors:

- overdue tasks
- tasks due today
- tasks due within the upcoming window
- completed tasks excluded from alert calculations

Reminders are created and stored through APScheduler, and duplicates are prevented by checking for existing reminder records before creating a new one.

## Analytics

Dashboard analytics are generated from actual task records in the database and include:

- summary metrics
- completion trend
- weekly productivity
- importance distribution
- status distribution
- overdue analysis

No hardcoded dashboard statistics are used in the live application.

## Testing

Run the full backend test suite:

```bash
pytest backend/tests -q
```

Current verified suite status:

- 15 tests passing

## Documentation

- Architecture overview: [docs/architecture.md](docs/architecture.md)
- API reference: [docs/api_documentation.md](docs/api_documentation.md)

## Notes for Demo or Evaluation

SMARTFLOW is structured as a professional academic project application with a working backend, dashboard, reminder logic, analytics, and API documentation. It is suitable for demonstration as a full-stack Python project while keeping the implementation simple and maintainable.
