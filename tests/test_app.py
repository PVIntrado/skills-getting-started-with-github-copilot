import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Tennis Club" in data
    assert "Basketball Team" in data


def test_signup_for_activity():
    activity = "Tennis Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400


def test_unregister_for_activity():
    activity = "Tennis Club"
    email = "newstudent@mergington.edu"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]
    # Unregister again should fail
    response2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 400


def test_signup_invalid_activity():
    response = client.post("/activities/InvalidActivity/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_unregister_invalid_activity():
    response = client.delete("/activities/InvalidActivity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
