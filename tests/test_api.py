from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rep_performance():
    response = client.get("/api/rep_performance/?rep_id=1")
    assert response.status_code == 200
    assert "feedback" in response.json()

def test_team_performance():
    response = client.get("/api/team_performance/")
    assert response.status_code == 200
    assert "team_feedback" in response.json()
