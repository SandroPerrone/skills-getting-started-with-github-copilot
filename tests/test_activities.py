def test_root_redirects_to_index(client):
    # Arrange — no preconditions needed

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"].endswith("/static/index.html")


def test_get_activities_returns_all(client):
    # Arrange — no preconditions needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    first = next(iter(data.values()))
    assert "description" in first
    assert "schedule" in first
    assert "max_participants" in first
    assert "participants" in first


def test_get_activities_returns_no_cache_headers(client):
    # Arrange — no preconditions needed

    # Act
    response = client.get("/activities")

    # Assert
    assert "no-store" in response.headers.get("cache-control", "")


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    activities_response = client.get("/activities").json()
    assert email in activities_response[activity_name]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/NonExistentActivity/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_allows_duplicate_registration(client):
    # Arrange — document current behavior: duplicate signup is permitted
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert participants.count(email) == 2


def test_unregister_removes_participant(client):
    # Arrange — sign up a participant so we can remove them
    activity_name = "Chess Club"
    email = "todelete@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_nonexistent_activity_returns_404(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/NonExistentActivity/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
