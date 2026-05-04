"""Tests for participant removal endpoint"""


def test_unregister_success(client):
    """Test successful removal of a participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Known participant

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Removed {email} from {activity_name}" in data["message"]

    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_student_not_found(client):
    """Test unregister when student is not signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "notsignedup@example.com"  # Not in Chess Club

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Student not found in this activity" in data["detail"]