import pytest
from fastapi.testclient import TestClient
from tasks.sample_data import generate_all_sample_data
from sqlalchemy.orm import sessionmaker
from database import engine
from app.user.models import User, Profile
from app.church.models import Church
from app.community.models import Board, Post, Comment
from app.verification.models import IdentityVerification
from app.action.models import ActionLog


class TestSampleDataGeneration:
    """Test sample data generation functionality"""
    
    def test_generate_sample_data_task(self, client: TestClient):
        """Test the sample data generation task endpoint"""
        response = client.post("/generate-sample-data")
        assert response.status_code == 200
        
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "Sample data generation started"
        assert "message" in data
    
    def test_cleanup_data_task(self, client: TestClient):
        """Test the data cleanup task endpoint"""
        response = client.post("/cleanup-data")
        assert response.status_code == 200
        
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "Data cleanup started"
        assert "message" in data
    
    def test_sample_data_generation_direct(self, db_session):
        """Test direct sample data generation"""
        # This test runs the sample data generation directly
        # Note: This might take a while and create a lot of data
        
        # Count initial records
        initial_users = db_session.query(User).count()
        initial_churches = db_session.query(Church).count()
        initial_boards = db_session.query(Board).count()
        
        # Generate sample data (using a smaller dataset for testing)
        from tasks.sample_data import (
            generate_sample_churches, 
            generate_sample_users,
            generate_sample_boards
        )
        
        # Generate smaller amounts for testing
        churches = generate_sample_churches(db_session, 2)
        users = generate_sample_users(db_session, 5)
        boards = generate_sample_boards(db_session, 3)
        
        # Verify data was created
        assert len(churches) == 2
        assert len(users) == 5  # 4 regular + 1 admin
        assert len(boards) == 3
        
        # Verify in database
        final_users = db_session.query(User).count()
        final_churches = db_session.query(Church).count()
        final_boards = db_session.query(Board).count()
        
        assert final_users == initial_users + 5
        assert final_churches == initial_churches + 2
        assert final_boards == initial_boards + 3
    
    def test_sample_churches_generation(self, db_session):
        """Test church generation specifically"""
        from tasks.sample_data import generate_sample_churches
        
        churches = generate_sample_churches(db_session, 3)
        
        assert len(churches) == 3
        for church in churches:
            assert church.name is not None
            assert church.id is not None
            # Verify it's actually in the database
            db_church = db_session.query(Church).filter(Church.id == church.id).first()
            assert db_church is not None
    
    def test_sample_users_generation(self, db_session):
        """Test user generation specifically"""
        from tasks.sample_data import generate_sample_users
        
        users = generate_sample_users(db_session, 10)
        
        assert len(users) == 10
        
        # Check that we have one admin user
        admin_users = [u for u in users if u.is_admin]
        assert len(admin_users) == 1
        
        # Check that most users are not blocked
        blocked_users = [u for u in users if u.is_blocked]
        assert len(blocked_users) < len(users)  # Should be less than total
        
        # Verify users are in database
        for user in users:
            db_user = db_session.query(User).filter(User.id == user.id).first()
            assert db_user is not None
    
    def test_sample_profiles_generation(self, db_session):
        """Test profile generation specifically"""
        from tasks.sample_data import (
            generate_sample_churches,
            generate_sample_users, 
            generate_sample_profiles
        )
        
        # Create dependencies first
        churches = generate_sample_churches(db_session, 2)
        users = generate_sample_users(db_session, 5)
        
        # Generate profiles
        profiles = generate_sample_profiles(db_session, users, churches)
        
        assert len(profiles) == len(users)
        
        # Verify profiles are linked to users
        for profile in profiles:
            assert profile.user_id in [u.id for u in users]
            assert profile.nickname is not None
            
            # Verify in database
            db_profile = db_session.query(Profile).filter(Profile.id == profile.id).first()
            assert db_profile is not None
    
    def test_sample_boards_generation(self, db_session):
        """Test board generation specifically"""
        from tasks.sample_data import generate_sample_boards
        
        boards = generate_sample_boards(db_session, 5)
        
        assert len(boards) == 5
        
        # Check board content
        board_titles = [b.title for b in boards]
        expected_titles = [
            "General Discussion",
            "Prayer Requests", 
            "Bible Study",
            "Youth Ministry",
            "Worship & Music"
        ]
        
        for title in expected_titles:
            assert title in board_titles
        
        # Verify in database
        for board in boards:
            db_board = db_session.query(Board).filter(Board.id == board.id).first()
            assert db_board is not None
            assert db_board.title is not None
            assert db_board.description is not None
    
    def test_sample_posts_generation(self, db_session):
        """Test post generation specifically"""
        from tasks.sample_data import (
            generate_sample_churches,
            generate_sample_users,
            generate_sample_boards,
            generate_sample_posts
        )
        
        # Create dependencies
        churches = generate_sample_churches(db_session, 2)
        users = generate_sample_users(db_session, 5)
        boards = generate_sample_boards(db_session, 3)
        
        # Generate posts
        posts = generate_sample_posts(db_session, boards, users, 10)
        
        assert len(posts) == 10
        
        # Verify posts are linked correctly
        for post in posts:
            assert post.board_id in [b.id for b in boards]
            assert post.author_id in [u.id for u in users if not u.is_blocked]
            assert post.title is not None
            assert post.contents is not None
            assert post.view_count >= 0
            assert post.like_count >= 0
            
            # Verify in database
            db_post = db_session.query(Post).filter(Post.id == post.id).first()
            assert db_post is not None
    
    def test_sample_comments_generation(self, db_session):
        """Test comment generation specifically"""
        from tasks.sample_data import (
            generate_sample_churches,
            generate_sample_users,
            generate_sample_boards,
            generate_sample_posts,
            generate_sample_comments
        )
        
        # Create dependencies
        churches = generate_sample_churches(db_session, 2)
        users = generate_sample_users(db_session, 5)
        boards = generate_sample_boards(db_session, 3)
        posts = generate_sample_posts(db_session, boards, users, 5)
        
        # Generate comments
        comments = generate_sample_comments(db_session, posts, users, 15)
        
        assert len(comments) == 15
        
        # Verify comments are linked correctly
        for comment in comments:
            assert comment.post_id in [p.id for p in posts]
            assert comment.author_id in [u.id for u in users if not u.is_blocked]
            assert comment.contents is not None
            
            # Verify in database
            db_comment = db_session.query(Comment).filter(Comment.id == comment.id).first()
            assert db_comment is not None
    
    def test_sample_verifications_generation(self, db_session):
        """Test verification generation specifically"""
        from tasks.sample_data import (
            generate_sample_churches,
            generate_sample_users,
            generate_sample_verifications
        )
        
        # Create dependencies
        churches = generate_sample_churches(db_session, 2)
        users = generate_sample_users(db_session, 10)
        
        # Generate verifications
        verifications = generate_sample_verifications(db_session, users, churches)
        
        # Should create verifications for some users (not all)
        assert len(verifications) <= len(users)
        assert len(verifications) > 0
        
        # Verify verifications are linked correctly
        for verification in verifications:
            assert verification.user_id in [u.id for u in users]
            assert verification.photo_url is not None
            assert verification.status in ["pending", "approved", "rejected"]
            
            # Verify in database
            db_verification = db_session.query(IdentityVerification).filter(
                IdentityVerification.id == verification.id
            ).first()
            assert db_verification is not None
    
    def test_sample_actions_generation(self, db_session):
        """Test action log generation specifically"""
        from tasks.sample_data import (
            generate_sample_churches,
            generate_sample_users,
            generate_sample_boards,
            generate_sample_posts,
            generate_sample_comments,
            generate_sample_actions
        )
        
        # Create dependencies
        churches = generate_sample_churches(db_session, 2)
        users = generate_sample_users(db_session, 5)
        boards = generate_sample_boards(db_session, 2)
        posts = generate_sample_posts(db_session, boards, users, 3)
        comments = generate_sample_comments(db_session, posts, users, 5)
        
        # Generate actions
        actions = generate_sample_actions(db_session, posts, comments, users)
        
        assert len(actions) > 0
        
        # Verify actions are linked correctly
        for action in actions:
            assert action.user_id in [u.id for u in users if not u.is_blocked]
            assert action.action_type in ["view", "like", "bookmark", "report"]
            assert action.target_type in ["post", "comment"]
            
            if action.target_type == "post":
                assert action.target_id in [p.id for p in posts]
            else:
                assert action.target_id in [c.id for c in comments]
            
            # Verify in database
            db_action = db_session.query(ActionLog).filter(ActionLog.id == action.id).first()
            assert db_action is not None


class TestDataIntegrity:
    """Test data integrity after sample data generation"""
    
    def test_foreign_key_relationships(self, db_session):
        """Test that all foreign key relationships are valid"""
        from tasks.sample_data import generate_all_sample_data
        
        # Generate a small dataset
        # Note: This creates actual data, so we need to be careful in tests
        
        # Instead, let's test the relationships with manually created data
        from tasks.sample_data import (
            generate_sample_churches,
            generate_sample_users,
            generate_sample_profiles
        )
        
        churches = generate_sample_churches(db_session, 1)
        users = generate_sample_users(db_session, 2)
        profiles = generate_sample_profiles(db_session, users, churches)
        
        # Verify all profiles have valid user_ids
        for profile in profiles:
            user = db_session.query(User).filter(User.id == profile.user_id).first()
            assert user is not None
            
            # If profile has a church_id, verify it exists
            if profile.church_id:
                church = db_session.query(Church).filter(Church.id == profile.church_id).first()
                assert church is not None
    
    def test_data_consistency(self, db_session):
        """Test data consistency rules"""
        from tasks.sample_data import (
            generate_sample_users,
            generate_sample_boards,
            generate_sample_posts
        )
        
        users = generate_sample_users(db_session, 5)
        boards = generate_sample_boards(db_session, 2)
        posts = generate_sample_posts(db_session, boards, users, 5)
        
        # Verify no blocked users created posts
        for post in posts:
            author = db_session.query(User).filter(User.id == post.author_id).first()
            assert author is not None
            assert not author.is_blocked
        
        # Verify all posts have valid boards
        for post in posts:
            board = db_session.query(Board).filter(Board.id == post.board_id).first()
            assert board is not None
