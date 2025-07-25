from celery import Celery
from sqlalchemy.orm import sessionmaker
from database import engine
from app.user.service import UserService, ProfileService
from app.church.service import ChurchService
from app.community.service import BoardService, PostService, CommentService, PostTagService
from app.verification.service import IdentityVerificationService
from app.action.service import ActionLogService
from app.user.schemas import UserCreate, ProfileCreate
from app.church.schemas import ChurchCreate
from app.community.schemas import BoardCreate, PostCreate, CommentCreate
from app.verification.schemas import IdentityVerificationCreate
from app.action.schemas import ActionLogCreate
import uuid
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def generate_sample_churches(db, count=5):
    """Generate sample churches"""
    churches = []
    church_names = [
        "First Baptist Church",
        "Grace Community Church", 
        "New Life Fellowship",
        "Trinity Methodist Church",
        "Hope Presbyterian Church",
        "Faith Lutheran Church",
        "Calvary Chapel",
        "St. Mary's Catholic Church"
    ]
    
    for i in range(min(count, len(church_names))):
        church_data = ChurchCreate(
            name=church_names[i],
            address=fake.address(),
            phone_number=fake.phone_number()
        )
        church = ChurchService.create_church(db, church_data)
        churches.append(church)
        print(f"Created church: {church.name}")
    
    return churches

def generate_sample_users(db, count=20):
    """Generate sample users"""
    users = []
    
    # Create admin user
    admin_user_data = UserCreate(is_blocked=False, is_admin=True)
    admin_user = UserService.create_user(db, admin_user_data)
    users.append(admin_user)
    print(f"Created admin user: {admin_user.id}")
    
    # Create regular users
    for i in range(count - 1):
        user_data = UserCreate(
            is_blocked=random.choice([False, False, False, True]),  # 25% chance of being blocked
            is_admin=False
        )
        user = UserService.create_user(db, user_data)
        users.append(user)
    
    print(f"Created {len(users)} users")
    return users

def generate_sample_profiles(db, users, churches):
    """Generate sample profiles for users"""
    profiles = []
    
    for user in users:
        profile_data = ProfileCreate(
            user_id=user.id,
            nickname=fake.user_name(),
            thumbnail=fake.image_url(width=200, height=200),
            church_id=random.choice(churches).id if churches and random.choice([True, False]) else None
        )
        profile = ProfileService.create_profile(db, profile_data)
        profiles.append(profile)
    
    print(f"Created {len(profiles)} profiles")
    return profiles

def generate_sample_boards(db, count=8):
    """Generate sample discussion boards"""
    boards = []
    board_topics = [
        ("General Discussion", "General community discussions and announcements"),
        ("Prayer Requests", "Share your prayer requests with the community"),
        ("Bible Study", "Discussion about Bible studies and scripture"),
        ("Youth Ministry", "Activities and discussions for young people"),
        ("Worship & Music", "Everything about worship services and music"),
        ("Community Service", "Volunteer opportunities and community outreach"),
        ("Family Life", "Discussions about family, parenting, and relationships"),
        ("Testimonies", "Share your faith journey and testimonies")
    ]
    
    for i in range(min(count, len(board_topics))):
        title, description = board_topics[i]
        board_data = BoardCreate(title=title, description=description)
        board = BoardService.create_board(db, board_data)
        boards.append(board)
        print(f"Created board: {board.title}")
    
    return boards

def generate_sample_posts(db, boards, users, count=50):
    """Generate sample posts"""
    posts = []
    
    post_titles = [
        "Welcome to our community!",
        "Sunday service announcement",
        "Prayer request for healing",
        "Bible study group forming",
        "Youth camp registration open",
        "Volunteer needed for food drive",
        "Testimony: God's faithfulness",
        "New member introduction",
        "Church picnic planning",
        "Mission trip update",
        "Worship team auditions",
        "Small group meeting times",
        "Community service project",
        "Easter celebration plans",
        "Christmas program volunteers"
    ]
    
    post_contents = [
        "Hello everyone! I'm excited to be part of this wonderful community. Looking forward to connecting with all of you and growing together in faith.",
        "Join us this Sunday for a special service. We'll be having guest speakers and special music. Service starts at 10 AM.",
        "Please keep my family in your prayers as we go through a difficult time. Your support means everything to us.",
        "Starting a new Bible study group focused on the book of Romans. We'll meet every Wednesday evening at 7 PM.",
        "Youth camp registration is now open! This will be an amazing week of fun, fellowship, and spiritual growth.",
        "We're organizing a food drive for the local shelter. Any donations of non-perishable items would be greatly appreciated.",
        "I wanted to share how God has been working in my life recently. His faithfulness never ceases to amaze me.",
        "Hi everyone! I'm new to the church and excited to get involved. What are some good ways to connect with the community?",
        "Planning our annual church picnic. We need volunteers for setup, food preparation, and activities. Please let me know if you can help!",
        "Update from our recent mission trip: We were able to help build three homes and share the gospel with many families.",
        "Our worship team is looking for new members. If you play an instrument or love to sing, please consider joining us!",
        "Small group meeting times have been updated. Please check the schedule and let me know which group you'd like to join.",
        "We're organizing a community service project to help clean up the local park. Join us this Saturday at 9 AM.",
        "Easter is coming! We're planning a special celebration and need volunteers for decorations and the Easter egg hunt.",
        "Our Christmas program is in the works. We need volunteers for costumes, set design, and coordination."
    ]
    
    for i in range(count):
        board = random.choice(boards)
        author = random.choice([u for u in users if not u.is_blocked])
        
        post_data = PostCreate(
            board_id=board.id,
            title=random.choice(post_titles),
            contents=random.choice(post_contents)
        )
        post = PostService.create_post(db, post_data, author.id)
        
        # Add some random view counts and likes
        post.view_count = random.randint(5, 100)
        post.like_count = random.randint(0, 20)
        db.commit()
        
        posts.append(post)
    
    print(f"Created {len(posts)} posts")
    return posts

def generate_sample_comments(db, posts, users, count=100):
    """Generate sample comments"""
    comments = []
    
    comment_texts = [
        "Thank you for sharing this!",
        "I'll be praying for you.",
        "Count me in!",
        "This is wonderful news.",
        "I'd love to help with this.",
        "Amen to that!",
        "Great idea, let's make it happen.",
        "I'm interested in joining.",
        "Thanks for the update.",
        "God bless you!",
        "I'll be there!",
        "This touched my heart.",
        "Let me know how I can help.",
        "Praise God!",
        "I'm excited about this opportunity."
    ]
    
    for i in range(count):
        post = random.choice(posts)
        author = random.choice([u for u in users if not u.is_blocked])
        
        comment_data = CommentCreate(
            post_id=post.id,
            contents=random.choice(comment_texts),
            parent_id=None  # For now, no nested comments
        )
        comment = CommentService.create_comment(db, comment_data, author.id)
        comments.append(comment)
    
    print(f"Created {len(comments)} comments")
    return comments

def generate_sample_tags(db, posts):
    """Generate sample tags for posts"""
    tags = []
    tag_names = [
        "announcement", "prayer", "volunteer", "youth", "worship", 
        "community", "bible-study", "testimony", "service", "fellowship",
        "family", "music", "outreach", "missions", "celebration"
    ]
    
    for post in posts:
        # Add 1-3 random tags per post
        num_tags = random.randint(1, 3)
        selected_tags = random.sample(tag_names, num_tags)
        
        for tag_name in selected_tags:
            try:
                tag = PostTagService.add_tag(db, post.id, tag_name)
                tags.append(tag)
            except:
                # Tag might already exist, skip
                pass
    
    print(f"Created tags for posts")
    return tags

def generate_sample_verifications(db, users, churches):
    """Generate sample identity verifications"""
    verifications = []
    
    # Create verifications for some users
    verification_users = random.sample(users, min(10, len(users)))
    
    for user in verification_users:
        verification_data = IdentityVerificationCreate(
            user_id=user.id,
            photo_url=fake.image_url(width=400, height=300),
            church_id=random.choice(churches).id if churches else None
        )
        verification = IdentityVerificationService.create_verification(db, verification_data)
        
        # Randomly approve/reject some verifications
        if random.choice([True, False, False]):  # 33% chance of being reviewed
            from app.verification.schemas import IdentityVerificationUpdate, VerificationStatus
            admin_user = next((u for u in users if u.is_admin), None)
            if admin_user:
                status = random.choice([VerificationStatus.APPROVED, VerificationStatus.REJECTED])
                update_data = IdentityVerificationUpdate(
                    status=status,
                    reviewed_by=admin_user.id
                )
                verification = IdentityVerificationService.update_verification_status(
                    db, verification.id, update_data
                )
        
        verifications.append(verification)
    
    print(f"Created {len(verifications)} identity verifications")
    return verifications

def generate_sample_actions(db, posts, comments, users):
    """Generate sample action logs"""
    actions = []
    action_types = ["view", "like", "bookmark", "report"]
    
    # Generate actions for posts
    for post in posts:
        # Each post gets 5-20 random actions
        num_actions = random.randint(5, 20)
        action_users = random.sample(users, min(num_actions, len(users)))
        
        for user in action_users:
            if user.is_blocked:
                continue
                
            action_type = random.choice(action_types)
            action_data = ActionLogCreate(
                user_id=user.id,
                action_type=action_type,
                target_type="post",
                target_id=post.id,
                is_on=random.choice([True, True, True, False])  # 75% chance of being active
            )
            action = ActionLogService.create_action_log(db, action_data)
            actions.append(action)
    
    # Generate actions for comments
    for comment in comments[:20]:  # Only for first 20 comments to avoid too much data
        num_actions = random.randint(1, 5)
        action_users = random.sample(users, min(num_actions, len(users)))
        
        for user in action_users:
            if user.is_blocked:
                continue
                
            action_type = random.choice(["like", "report"])  # Comments don't have views/bookmarks
            action_data = ActionLogCreate(
                user_id=user.id,
                action_type=action_type,
                target_type="comment",
                target_id=comment.id,
                is_on=True
            )
            action = ActionLogService.create_action_log(db, action_data)
            actions.append(action)
    
    print(f"Created {len(actions)} action logs")
    return actions

def generate_all_sample_data():
    """Generate all sample data"""
    db = SessionLocal()
    
    try:
        print("🚀 Starting sample data generation...")
        print("=" * 50)
        
        # Generate data in order of dependencies
        churches = generate_sample_churches(db, 5)
        users = generate_sample_users(db, 20)
        profiles = generate_sample_profiles(db, users, churches)
        boards = generate_sample_boards(db, 8)
        posts = generate_sample_posts(db, boards, users, 50)
        comments = generate_sample_comments(db, posts, users, 100)
        tags = generate_sample_tags(db, posts)
        verifications = generate_sample_verifications(db, users, churches)
        actions = generate_sample_actions(db, posts, comments, users)
        
        print("=" * 50)
        print("🎉 Sample data generation completed!")
        print(f"Generated:")
        print(f"  - {len(churches)} churches")
        print(f"  - {len(users)} users")
        print(f"  - {len(profiles)} profiles")
        print(f"  - {len(boards)} boards")
        print(f"  - {len(posts)} posts")
        print(f"  - {len(comments)} comments")
        print(f"  - {len(verifications)} verifications")
        print(f"  - {len(actions)} action logs")
        
        return {
            "churches": len(churches),
            "users": len(users),
            "profiles": len(profiles),
            "boards": len(boards),
            "posts": len(posts),
            "comments": len(comments),
            "verifications": len(verifications),
            "actions": len(actions)
        }
        
    except Exception as e:
        print(f"❌ Error generating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    generate_all_sample_data()
