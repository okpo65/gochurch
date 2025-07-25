import pytest
from fastapi.testclient import TestClient
import uuid
from app.user.models import User, Profile


class TestUsers:
    """Test user management endpoints"""
    
    def test_create_user(self, client: TestClient):
        """Test creating a new user"""
        user_data = {
            "is_blocked": False,
            "is_admin": False
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["is_blocked"] == False
        assert data["is_admin"] == False
        assert "created_at" in data
        
        # Verify UUID format
        user_id = uuid.UUID(data["id"])
        assert isinstance(user_id, uuid.UUID)
    
    def test_create_admin_user(self, client: TestClient):
        """Test creating an admin user"""
        user_data = {
            "is_blocked": False,
            "is_admin": True
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["is_admin"] == True
    
    def test_get_users(self, client: TestClient):
        """Test getting list of users"""
        # Create a few users first
        for i in range(3):
            user_data = {"is_blocked": False, "is_admin": False}
            client.post("/users/", json=user_data)
        
        response = client.get("/users/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3
    
    def test_get_user_by_id(self, client: TestClient):
        """Test getting a specific user by ID"""
        # Create a user first
        user_data = {"is_blocked": False, "is_admin": False}
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Get the user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == user_id
    
    def test_get_nonexistent_user(self, client: TestClient):
        """Test getting a user that doesn't exist"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/users/{fake_id}")
        assert response.status_code == 404
    
    def test_update_user(self, client: TestClient):
        """Test updating a user"""
        # Create a user first
        user_data = {"is_blocked": False, "is_admin": False}
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Update the user
        update_data = {"is_blocked": True}
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["is_blocked"] == True
        assert data["is_admin"] == False  # Should remain unchanged
    
    def test_delete_user(self, client: TestClient):
        """Test deleting a user"""
        # Create a user first
        user_data = {"is_blocked": False, "is_admin": False}
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Delete the user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert "message" in response.json()
        
        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404


class TestProfiles:
    """Test user profile endpoints"""
    
    def test_create_profile(self, client: TestClient):
        """Test creating a user profile"""
        # Create a user first
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        # Create a church for the profile
        church_data = {
            "name": "Test Church",
            "address": "123 Test St",
            "phone_number": "+1-555-0123"
        }
        church_response = client.post("/churches/", json=church_data)
        church_id = church_response.json()["id"]
        
        # Create profile
        profile_data = {
            "user_id": user_id,
            "nickname": "testuser",
            "thumbnail": "https://example.com/avatar.jpg",
            "church_id": church_id
        }
        
        response = client.post("/users/profiles/", json=profile_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["user_id"] == user_id
        assert data["nickname"] == "testuser"
        assert data["church_id"] == church_id
    
    def test_get_profile_by_id(self, client: TestClient):
        """Test getting a profile by ID"""
        # Create user and profile
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        profile_data = {
            "user_id": user_id,
            "nickname": "testuser"
        }
        profile_response = client.post("/users/profiles/", json=profile_data)
        profile_id = profile_response.json()["id"]
        
        # Get profile
        response = client.get(f"/users/profiles/{profile_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == profile_id
        assert data["nickname"] == "testuser"
    
    def test_get_user_profile(self, client: TestClient):
        """Test getting a user's profile"""
        # Create user and profile
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        profile_data = {
            "user_id": user_id,
            "nickname": "testuser"
        }
        client.post("/users/profiles/", json=profile_data)
        
        # Get user's profile
        response = client.get(f"/users/{user_id}/profile")
        assert response.status_code == 200
        
        data = response.json()
        assert data["user_id"] == user_id
        assert data["nickname"] == "testuser"
    
    def test_update_profile(self, client: TestClient):
        """Test updating a profile"""
        # Create user and profile
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        profile_data = {
            "user_id": user_id,
            "nickname": "testuser"
        }
        profile_response = client.post("/users/profiles/", json=profile_data)
        profile_id = profile_response.json()["id"]
        
        # Update profile
        update_data = {"nickname": "updated_user"}
        response = client.put(f"/users/profiles/{profile_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["nickname"] == "updated_user"
    
    def test_delete_profile(self, client: TestClient):
        """Test deleting a profile"""
        # Create user and profile
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        profile_data = {
            "user_id": user_id,
            "nickname": "testuser"
        }
        profile_response = client.post("/users/profiles/", json=profile_data)
        profile_id = profile_response.json()["id"]
        
        # Delete profile
        response = client.delete(f"/users/profiles/{profile_id}")
        assert response.status_code == 200
        
        # Verify profile is deleted
        get_response = client.get(f"/users/profiles/{profile_id}")
        assert get_response.status_code == 404
