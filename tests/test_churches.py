import pytest
from fastapi.testclient import TestClient
import uuid


class TestChurches:
    """Test church management endpoints"""
    
    def test_create_church(self, client: TestClient):
        """Test creating a new church"""
        church_data = {
            "name": "First Baptist Church",
            "address": "123 Main Street, Anytown, USA",
            "phone_number": "+1-555-0123"
        }
        
        response = client.post("/churches/", json=church_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["name"] == "First Baptist Church"
        assert data["address"] == "123 Main Street, Anytown, USA"
        assert data["phone_number"] == "+1-555-0123"
        
        # Verify UUID format
        church_id = uuid.UUID(data["id"])
        assert isinstance(church_id, uuid.UUID)
    
    def test_create_church_minimal(self, client: TestClient):
        """Test creating a church with only required fields"""
        church_data = {
            "name": "Grace Community Church"
        }
        
        response = client.post("/churches/", json=church_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == "Grace Community Church"
        assert data["address"] is None
        assert data["phone_number"] is None
    
    def test_get_churches(self, client: TestClient):
        """Test getting list of churches"""
        # Create a few churches first
        churches = [
            {"name": "Church 1", "address": "Address 1"},
            {"name": "Church 2", "address": "Address 2"},
            {"name": "Church 3", "address": "Address 3"}
        ]
        
        for church_data in churches:
            client.post("/churches/", json=church_data)
        
        response = client.get("/churches/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3
    
    def test_get_church_by_id(self, client: TestClient):
        """Test getting a specific church by ID"""
        # Create a church first
        church_data = {
            "name": "Test Church",
            "address": "Test Address",
            "phone_number": "+1-555-9999"
        }
        create_response = client.post("/churches/", json=church_data)
        church_id = create_response.json()["id"]
        
        # Get the church
        response = client.get(f"/churches/{church_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == church_id
        assert data["name"] == "Test Church"
    
    def test_get_nonexistent_church(self, client: TestClient):
        """Test getting a church that doesn't exist"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/churches/{fake_id}")
        assert response.status_code == 404
    
    def test_update_church(self, client: TestClient):
        """Test updating a church"""
        # Create a church first
        church_data = {
            "name": "Original Church",
            "address": "Original Address"
        }
        create_response = client.post("/churches/", json=church_data)
        church_id = create_response.json()["id"]
        
        # Update the church
        update_data = {
            "name": "Updated Church",
            "phone_number": "+1-555-1111"
        }
        response = client.put(f"/churches/{church_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Updated Church"
        assert data["phone_number"] == "+1-555-1111"
        assert data["address"] == "Original Address"  # Should remain unchanged
    
    def test_delete_church(self, client: TestClient):
        """Test deleting a church"""
        # Create a church first
        church_data = {"name": "Church to Delete"}
        create_response = client.post("/churches/", json=church_data)
        church_id = create_response.json()["id"]
        
        # Delete the church
        response = client.delete(f"/churches/{church_id}")
        assert response.status_code == 200
        assert "message" in response.json()
        
        # Verify church is deleted
        get_response = client.get(f"/churches/{church_id}")
        assert get_response.status_code == 404
    
    def test_church_pagination(self, client: TestClient):
        """Test church list pagination"""
        # Create multiple churches
        for i in range(10):
            church_data = {"name": f"Church {i}"}
            client.post("/churches/", json=church_data)
        
        # Test pagination
        response = client.get("/churches/?skip=5&limit=3")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) <= 3
    
    def test_create_church_validation(self, client: TestClient):
        """Test church creation validation"""
        # Test missing required field
        response = client.post("/churches/", json={})
        assert response.status_code == 422
        
        # Test invalid data types
        invalid_data = {"name": 123}  # name should be string
        response = client.post("/churches/", json=invalid_data)
        assert response.status_code == 422
