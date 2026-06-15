"""Unit tests for application logic and data structures."""

from src.app import activities


def test_activities_structure():
    """Test that the activities data structure has the expected format."""
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_all_activities_have_initial_participants():
    """Test that all activities have at least some initial participants."""
    for activity_name, activity_data in activities.items():
        participants = activity_data["participants"]
        assert len(participants) > 0, f"{activity_name} has no initial participants"


def test_participant_email_format():
    """Test that all initial participant emails have the expected format."""
    for activity_name, activity_data in activities.items():
        for email in activity_data["participants"]:
            assert isinstance(email, str)
            assert "@mergington.edu" in email
            assert len(email.split("@")[0]) > 0  # Name part should have at least one char


def test_specific_activities_exist():
    """Test that expected activities are present in the database."""
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Track & Field",
        "Art Club",
        "Drama Club",
        "Math Olympiad",
        "Science Club"
    ]
    
    for activity in expected_activities:
        assert activity in activities, f"{activity} not found in activities"


def test_max_participants_is_reasonable():
    """Test that max_participants values are reasonable."""
    for activity_name, activity_data in activities.items():
        max_part = activity_data["max_participants"]
        assert isinstance(max_part, int)
        assert max_part > 0, f"{activity_name} has invalid max_participants"
        assert max_part <= 100, f"{activity_name} has unreasonably high max_participants"
