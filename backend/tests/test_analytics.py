from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_summary_metrics():
    response = client.get('/api/analytics/summary')
    assert response.status_code == 200
    payload = response.json()
    assert 'total_tasks' in payload
    assert 'completion_rate' in payload


def test_status_distribution():
    response = client.get('/api/analytics/status-distribution')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_importance_distribution():
    response = client.get('/api/analytics/importance-distribution')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
