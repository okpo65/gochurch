import pytest
from fastapi.testclient import TestClient
import uuid


class TestBoards:
    """Test board management endpoints"""
    
    def test_create_board(self, client: TestClient):
        """Test creating a new board"""
        board_data = {
            "title": "General Discussion",
            "description": "A place for general community discussions"
        }
        
        response = client.post("/boards/", json=board_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["title"] == "General Discussion"
        assert data["description"] == "A place for general community discussions"
        assert "created_at" in data
    
    def test_create_board_minimal(self, client: TestClient):
        """Test creating a board with only required fields"""
        board_data = {"title": "Prayer Requests"}
        
        response = client.post("/boards/", json=board_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == "Prayer Requests"
        assert data["description"] is None
    
    def test_get_boards(self, client: TestClient):
        """Test getting list of boards"""
        # Create a few boards first
        boards = [
            {"title": "Board 1", "description": "Description 1"},
            {"title": "Board 2", "description": "Description 2"},
            {"title": "Board 3", "description": "Description 3"}
        ]
        
        for board_data in boards:
            client.post("/boards/", json=board_data)
        
        response = client.get("/boards/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3
    
    def test_get_board_by_id(self, client: TestClient):
        """Test getting a specific board by ID"""
        board_data = {"title": "Test Board", "description": "Test Description"}
        create_response = client.post("/boards/", json=board_data)
        board_id = create_response.json()["id"]
        
        response = client.get(f"/boards/{board_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == board_id
        assert data["title"] == "Test Board"
    
    def test_update_board(self, client: TestClient):
        """Test updating a board"""
        board_data = {"title": "Original Board"}
        create_response = client.post("/boards/", json=board_data)
        board_id = create_response.json()["id"]
        
        update_data = {"title": "Updated Board", "description": "New description"}
        response = client.put(f"/boards/{board_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Updated Board"
        assert data["description"] == "New description"
    
    def test_delete_board(self, client: TestClient):
        """Test deleting a board"""
        board_data = {"title": "Board to Delete"}
        create_response = client.post("/boards/", json=board_data)
        board_id = create_response.json()["id"]
        
        response = client.delete(f"/boards/{board_id}")
        assert response.status_code == 200
        
        # Verify board is deleted
        get_response = client.get(f"/boards/{board_id}")
        assert get_response.status_code == 404


class TestPosts:
    """Test post management endpoints"""
    
    def setup_method(self):
        """Setup method to create required data for post tests"""
        pass
    
    def test_create_post(self, client: TestClient):
        """Test creating a new post"""
        # Create a board first
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        # Create a user for the author
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        # Create post
        post_data = {
            "board_id": board_id,
            "title": "Welcome Post",
            "contents": "Welcome to our community board!"
        }
        
        response = client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == "Welcome Post"
        assert data["contents"] == "Welcome to our community board!"
        assert data["board_id"] == board_id
        assert data["author_id"] == author_id
        assert data["like_count"] == 0
        assert data["comment_count"] == 0
        assert data["view_count"] == 0
    
    def test_get_posts_by_board(self, client: TestClient):
        """Test getting posts for a specific board"""
        # Create board and user
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        # Create multiple posts
        for i in range(3):
            post_data = {
                "board_id": board_id,
                "title": f"Post {i}",
                "contents": f"Content for post {i}"
            }
            client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        
        # Get posts
        response = client.get(f"/boards/{board_id}/posts")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
    
    def test_get_post_by_id(self, client: TestClient):
        """Test getting a specific post by ID"""
        # Create board, user, and post
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Get post (this should increment view count)
        response = client.get(f"/boards/posts/{post_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == post_id
        assert data["title"] == "Test Post"
        assert data["view_count"] == 1  # Should be incremented
    
    def test_update_post(self, client: TestClient):
        """Test updating a post"""
        # Create board, user, and post
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Original Post",
            "contents": "Original content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Update post
        update_data = {
            "title": "Updated Post",
            "contents": "Updated content"
        }
        response = client.put(f"/boards/posts/{post_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Updated Post"
        assert data["contents"] == "Updated content"


class TestComments:
    """Test comment management endpoints"""
    
    def test_create_comment(self, client: TestClient):
        """Test creating a comment on a post"""
        # Create board, user, and post
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Create comment
        comment_data = {
            "post_id": post_id,
            "contents": "Great post! Thanks for sharing."
        }
        
        response = client.post(f"/boards/posts/{post_id}/comments?author_id={author_id}", json=comment_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["contents"] == "Great post! Thanks for sharing."
        assert data["post_id"] == post_id
        assert data["author_id"] == author_id
        assert data["parent_id"] is None
    
    def test_get_comments_by_post(self, client: TestClient):
        """Test getting comments for a specific post"""
        # Create board, user, and post
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Create multiple comments
        for i in range(3):
            comment_data = {
                "post_id": post_id,
                "contents": f"Comment {i}"
            }
            client.post(f"/boards/posts/{post_id}/comments?author_id={author_id}", json=comment_data)
        
        # Get comments
        response = client.get(f"/boards/posts/{post_id}/comments")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
    
    def test_update_comment(self, client: TestClient):
        """Test updating a comment"""
        # Create board, user, post, and comment
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        comment_data = {
            "post_id": post_id,
            "contents": "Original comment"
        }
        comment_response = client.post(f"/boards/posts/{post_id}/comments?author_id={author_id}", json=comment_data)
        comment_id = comment_response.json()["id"]
        
        # Update comment
        update_data = {"contents": "Updated comment"}
        response = client.put(f"/boards/comments/{comment_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["contents"] == "Updated comment"


class TestPostTags:
    """Test post tagging endpoints"""
    
    def test_add_post_tag(self, client: TestClient):
        """Test adding a tag to a post"""
        # Create board, user, and post
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Add tag
        response = client.post(f"/boards/posts/{post_id}/tags?tag=announcement")
        assert response.status_code == 201
        
        data = response.json()
        assert data["post_id"] == post_id
        assert data["tag"] == "announcement"
    
    def test_get_post_tags(self, client: TestClient):
        """Test getting tags for a post"""
        # Create board, user, and post
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Add multiple tags
        tags = ["announcement", "important", "community"]
        for tag in tags:
            client.post(f"/boards/posts/{post_id}/tags?tag={tag}")
        
        # Get tags
        response = client.get(f"/boards/posts/{post_id}/tags")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
    
    def test_remove_post_tag(self, client: TestClient):
        """Test removing a tag from a post"""
        # Create board, user, and post
        board_data = {"title": "Test Board"}
        board_response = client.post("/boards/", json=board_data)
        board_id = board_response.json()["id"]
        
        user_data = {"is_blocked": False, "is_admin": False}
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "board_id": board_id,
            "title": "Test Post",
            "contents": "Test content"
        }
        post_response = client.post(f"/boards/{board_id}/posts?author_id={author_id}", json=post_data)
        post_id = post_response.json()["id"]
        
        # Add tag
        client.post(f"/boards/posts/{post_id}/tags?tag=test")
        
        # Remove tag
        response = client.delete(f"/boards/posts/{post_id}/tags/test")
        assert response.status_code == 200
        
        # Verify tag is removed
        get_response = client.get(f"/boards/posts/{post_id}/tags")
        data = get_response.json()
        assert len(data) == 0
