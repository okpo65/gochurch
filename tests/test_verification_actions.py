import pytest
from fastapi.testclient import TestClient
import uuid


class TestIdentityVerification:
    """Test identity verification endpoints"""
    
    def test_create_verification(self, client: TestClient):
        """Test creating an identity verification request"""
        # Create user and church first
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        church_data = {"name": "Test Church"}
        church_response = client.post("/churches/", json=church_data)
        church_id = church_response.json()["id"]
        
        # Create verification
        verification_data = {
            "user_id": user_id,
            "photo_url": "https://example.com/verification-photo.jpg",
            "church_id": church_id
        }
        
        response = client.post("/verifications/", json=verification_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["user_id"] == user_id
        assert data["photo_url"] == "https://example.com/verification-photo.jpg"
        assert data["church_id"] == church_id
        assert data["status"] == "pending"
        assert data["reviewed_by"] is None
        assert data["reviewed_at"] is None
    
    def test_get_pending_verifications(self, client: TestClient):
        """Test getting pending verification requests"""
        # Create user and verification
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        verification_data = {
            "user_id": user_id,
            "photo_url": "https://example.com/photo.jpg"
        }
        client.post("/verifications/", json=verification_data)
        
        # Get pending verifications
        response = client.get("/verifications/pending")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["status"] == "pending"
    
    def test_get_verifications_by_status(self, client: TestClient):
        """Test getting verifications by status"""
        # Create user and verification
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        verification_data = {
            "user_id": user_id,
            "photo_url": "https://example.com/photo.jpg"
        }
        client.post("/verifications/", json=verification_data)
        
        # Get verifications by status
        response = client.get("/verifications/status/pending")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_user_verifications(self, client: TestClient):
        """Test getting verifications for a specific user"""
        # Create user and verification
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        verification_data = {
            "user_id": user_id,
            "photo_url": "https://example.com/photo.jpg"
        }
        client.post("/verifications/", json=verification_data)
        
        # Get user verifications
        response = client.get(f"/verifications/user/{user_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["user_id"] == user_id
    
    def test_update_verification_status(self, client: TestClient):
        """Test updating verification status"""
        # Create users (regular and admin)
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        admin_data = {"is_blocked": False, "is_admin": True}
        admin_response = client.post("/users/", json=admin_data)
        admin_id = admin_response.json()["id"]
        
        # Create verification
        verification_data = {
            "user_id": user_id,
            "photo_url": "https://example.com/photo.jpg"
        }
        verification_response = client.post("/verifications/", json=verification_data)
        verification_id = verification_response.json()["id"]
        
        # Update verification status
        update_data = {
            "status": "approved",
            "reviewed_by": admin_id
        }
        response = client.put(f"/verifications/{verification_id}/status", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "approved"
        assert data["reviewed_by"] == admin_id
        assert data["reviewed_at"] is not None
    
    def test_get_verification_by_id(self, client: TestClient):
        """Test getting a specific verification by ID"""
        # Create user and verification
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        verification_data = {
            "user_id": user_id,
            "photo_url": "https://example.com/photo.jpg"
        }
        verification_response = client.post("/verifications/", json=verification_data)
        verification_id = verification_response.json()["id"]
        
        # Get verification
        response = client.get(f"/verifications/{verification_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == verification_id
        assert data["user_id"] == user_id


class TestActionLogs:
    """Test action log endpoints"""
    
    def test_create_action_log(self, client: TestClient):
        """Test creating an action log"""
        # Create user, board, and post
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={user_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Create action log
        action_data = {
            "user_id": user_id,
            "action_type": "like",
            "target_type": "post",
            "target_id": post_id,
            "is_on": True
        }
        
        response = client.post("/actions/", json=action_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["user_id"] == user_id
        assert data["action_type"] == "like"
        assert data["target_type"] == "post"
        assert data["target_id"] == post_id
        assert data["is_on"] == True
    
    def test_toggle_action(self, client: TestClient):
        """Test toggling an action (like/unlike)"""
        # Create user, board, and post
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={user_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Toggle action (first time - should create and set to True)
        response = client.post(f"/actions/toggle?user_id={user_id}&action_type=like&target_type=post&target_id={post_id}")
        assert response.status_code == 201
        
        data = response.json()
        assert data["is_on"] == True
        
        # Toggle again (should set to False)
        response = client.post(f"/actions/toggle?user_id={user_id}&action_type=like&target_type=post&target_id={post_id}")
        assert response.status_code == 201
        
        data = response.json()
        assert data["is_on"] == False
    
    def test_get_user_actions(self, client: TestClient):
        """Test getting actions for a specific user"""
        # Create user, board, and post
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={user_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Create multiple actions
        actions = ["like", "bookmark", "view"]
        for action in actions:
            client.post(f"/actions/toggle?user_id={user_id}&action_type={action}&target_type=post&target_id={post_id}")
        
        # Get user actions
        response = client.get(f"/actions/user/{user_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3
    
    def test_get_target_actions(self, client: TestClient):
        """Test getting actions for a specific target"""
        # Create users, board, and post
        user1_data = {"is_blocked": False, "is_admin": False}
        user1_response = client.post("/users/", json=user1_data)
        user1_id = user1_response.json()["id"]
        
        user2_data = {"is_blocked": False, "is_admin": False}
        user2_response = client.post("/users/", json=user2_data)
        user2_id = user2_response.json()["id"]
        
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={user1_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Create actions from different users
        client.post(f"/actions/toggle?user_id={user1_id}&action_type=like&target_type=post&target_id={post_id}")
        client.post(f"/actions/toggle?user_id={user2_id}&action_type=like&target_type=post&target_id={post_id}")
        
        # Get target actions
        response = client.get(f"/actions/target/post/{post_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
    
    def test_get_action_count(self, client: TestClient):
        """Test getting action count for a target"""
        # Create users, board, and post
        user1_data = {"is_blocked": False, "is_admin": False}
        user1_response = client.post("/users/", json=user1_data)
        user1_id = user1_response.json()["id"]
        
        user2_data = {"is_blocked": False, "is_admin": False}
        user2_response = client.post("/users/", json=user2_data)
        user2_id = user2_response.json()["id"]
        
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={user1_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Create likes from different users
        client.post(f"/actions/toggle?user_id={user1_id}&action_type=like&target_type=post&target_id={post_id}")
        client.post(f"/actions/toggle?user_id={user2_id}&action_type=like&target_type=post&target_id={post_id}")
        
        # Get like count
        response = client.get(f"/actions/count/post/{post_id}/like")
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] == 2
    
    def test_get_action_log_by_id(self, client: TestClient):
        """Test getting a specific action log by ID"""
        # Create user, board, and post
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={user_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Create action
        action_response = client.post(f"/actions/toggle?user_id={user_id}&action_type=like&target_type=post&target_id={post_id}")
        action_id = action_response.json()["id"]
        
        # Get action log
        response = client.get(f"/actions/{action_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == action_id
        assert data["user_id"] == user_id
