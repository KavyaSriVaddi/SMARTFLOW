# SMARTFLOW API Documentation

Base URL: http://localhost:8000

SMARTFLOW exposes a REST API for task management, reminders, analytics, and settings. All API routes are documented through the FastAPI OpenAPI schema and can be viewed in Swagger UI at:

- http://127.0.0.1:8000/docs

## Application Endpoints

### Health

- GET /health
  - Returns the service status for the backend application.

### Tasks

- POST /api/tasks
  - Create a new task.
  - Request body example:

```json
{
  "title": "Prepare final presentation",
  "description": "Create slides and rehearse the final demo",
  "due_date": "2026-12-01T12:00:00Z",
  "importance": "High",
  "status": "Pending",
  "estimated_duration": 3
}
```

- GET /api/tasks
  - List tasks with optional filters such as search, status, importance, overdue_only, due_today, and due_this_week.

- GET /api/tasks/{task_id}
  - Retrieve a single task.

- PUT /api/tasks/{task_id}
  - Update a task.

- DELETE /api/tasks/{task_id}
  - Delete a task.
  - Response status: 204 No Content

- PATCH /api/tasks/{task_id}/complete
  - Mark a task as completed.

- GET /api/tasks/prioritized
  - Return ranked tasks by priority score.

- GET /api/tasks/overdue
  - Return overdue tasks only.

- GET /api/tasks/due-soon
  - Return tasks due within the next seven days.

### Analytics

- GET /api/analytics/summary
  - Returns dashboard summary metrics.

- GET /api/analytics/status-distribution
  - Returns task counts by status.

- GET /api/analytics/importance-distribution
  - Returns task counts by importance.

- GET /api/analytics/completion-trend
  - Returns a completion trend over time.

- GET /api/analytics/weekly-productivity
  - Returns weekly productivity metrics.

- GET /api/analytics/overdue-analysis
  - Returns insights about overdue tasks.

### Reminders

- GET /api/reminders
  - List reminder notifications.

- PATCH /api/reminders/{reminder_id}/read
  - Mark a reminder as read.

- DELETE /api/reminders/{reminder_id}
  - Delete a reminder.
  - Response status: 204 No Content

### Settings

- GET /api/settings
  - Retrieve application settings.

- PUT /api/settings
  - Update system settings such as priority weights and reminder configuration.

## Example Response: Task

```json
{
  "id": 1,
  "title": "Prepare final presentation",
  "description": "Create slides and rehearse the final demo",
  "due_date": "2026-12-01T12:00:00Z",
  "importance": "High",
  "status": "Pending",
  "estimated_duration": 3,
  "priority_score": 87,
  "priority_category": "High",
  "priority_explanation": "Deadline is close and task importance is high.",
  "suggested_rank": 1
}
```

## HTTP Status Codes

The API uses standard HTTP status codes:

- 200 OK: successful read or update
- 201 Created: task created successfully
- 204 No Content: successful delete or reminder removal
- 404 Not Found: task or reminder not found
- 422 Unprocessable Entity: invalid payload or validation failure

## Notes

- The project uses actual database records for analytics, not hardcoded values.
- The Swagger schema reflects the live backend implementation.
- All task responses include priority metadata when a task is retrieved from the API.
