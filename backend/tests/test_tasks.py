from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_read_task():
    task = {
        'title': 'Write report',
        'description': 'Draft final report',
        'due_date': '2026-12-01T12:00:00Z',
        'importance': 'High',
        'status': 'Pending',
        'estimated_duration': 3,
    }
    response = client.post('/api/tasks', json=task)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['title'] == 'Write report'
    assert data['id'] > 0


def test_update_task():
    response = client.post(
        '/api/tasks',
        json={
            'title': 'Update notes',
            'description': 'Revise notes',
            'due_date': '2026-11-15T10:00:00Z',
            'importance': 'Medium',
            'status': 'Pending',
        },
    )
    task_id = response.json()['id']
    updated = client.put(f'/api/tasks/{task_id}', json={'status': 'In Progress'})
    assert updated.status_code == 200
    assert updated.json()['status'] == 'In Progress'


def test_delete_task():
    response = client.post(
        '/api/tasks',
        json={
            'title': 'Remove outdated task',
            'description': 'Delete after review',
            'due_date': '2026-11-17T09:00:00Z',
            'importance': 'Low',
            'status': 'Pending',
        },
    )
    task_id = response.json()['id']
    delete_response = client.delete(f'/api/tasks/{task_id}')
    assert delete_response.status_code == 204


def test_invalid_task_input():
    response = client.post(
        '/api/tasks',
        json={
            'title': '',
            'description': '',
            'due_date': '2026-11-01T00:00:00Z',
            'importance': 'Wrong',
            'status': 'Invalid',
        },
    )
    assert response.status_code == 422
