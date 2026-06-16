from fastapi.testclient import TestClient
from src import app as app_module

client = TestClient(app_module.app)


def test_get_activities():
    # Arrange: TestClient and fresh activities (fixture handles reset)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Check a known activity exists and has participants list
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success():
    # Arrange
    email = "newstudent@example.com"
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 200
    payload = resp.json()
    assert email in payload.get("message", "")

    # Verify via GET that participant was added
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    assert email in resp2.json()[activity]["participants"]


def test_signup_duplicate_rejected():
    # Arrange: use an existing participant from the initial seed state
    existing = app_module.activities["Chess Club"]["participants"][0]
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={existing}")

    # Assert
    assert resp.status_code == 400
    assert "already signed up" in resp.json().get("detail", "").lower()


def test_remove_participant_success():
    # Arrange: pick an existing participant
    activity = "Chess Club"
    existing = app_module.activities[activity]["participants"][0]

    # Act
    resp = client.delete(f"/activities/{activity}/participant?email={existing}")

    # Assert
    assert resp.status_code == 200
    assert existing in resp.json().get("message", "")

    # Verify via GET that participant was removed
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    assert existing not in resp2.json()[activity]["participants"]


def test_remove_nonexistent_participant():
    # Arrange
    activity = "Chess Club"
    email = "not-found@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/participant?email={email}")

    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()
