"""Integration tests for FastAPI endpoints."""

import pytest


def test_root_redirect(client):
    """Test that the root endpoint redirects to /static/index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_success(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    
    # Verify structure of an activity
    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_signup_success(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify the student was actually added
    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_email(client):
    """Test that signup fails when email is already registered."""
    # First, get the current participants to use an existing one
    activities = client.get("/activities").json()
    existing_email = activities["Chess Club"]["participants"][0]
    
    # Try to sign up with the same email
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": existing_email}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test that signup fails for a non-existent activity."""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant_success(client):
    """Test successful removal of a participant from an activity."""
    # First, signup a new participant
    email = "testremove@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    
    # Verify the student is signed up
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    
    # Remove the participant
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email}
    )
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    
    # Verify the student was actually removed
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_remove_nonexistent_participant(client):
    """Test that removal fails when participant is not found."""
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "nonexistent@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_from_nonexistent_activity(client):
    """Test that removal fails for a non-existent activity."""
    response = client.delete(
        "/activities/Nonexistent Activity/participants",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_multiple_signups_different_emails(client):
    """Test that multiple different emails can be added to an activity."""
    emails = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ]
    
    for email in emails:
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify all were added
    activities = client.get("/activities").json()
    participants = activities["Programming Class"]["participants"]
    for email in emails:
        assert email in participants
