#!/usr/bin/env python3
"""
Simple script to generate sample data for testing
Works with the remove_all_data.py script for easy cleanup and regeneration
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database import SessionLocal
from app.models import (
    User, Profile, Church, Board, Post, PostTag, Comment,
    IdentityVerification, ActionLog
)

def generate_sample_data(db_session):
    """Generate a comprehensive set of sample data"""
    
    print("🏗️  Generating sample data...")
    
    # Create Churches
    churches = [
        Church(name="First Baptist Church", address="123 Main Street, Springfield", phone_number="+1-555-0101"),
        Church(name="Grace Community Church", address="456 Oak Avenue, Springfield", phone_number="+1-555-0102"),
        Church(name="St. Mary's Catholic Church", address="789 Pine Road, Springfield", phone_number="+1-555-0103"),
    ]
    
    for church in churches:
        db_session.add(church)
    db_session.commit()
    
    for church in churches:
        db_session.refresh(church)
    print(f"✅ Created {len(churches)} churches")
    
    # Create Users
    users = [
        User(is_blocked=False, is_admin=True),   # Admin user
        User(is_blocked=False, is_admin=False),  # Regular users
        User(is_blocked=False, is_admin=False),
        User(is_blocked=False, is_admin=False),
        User(is_blocked=True, is_admin=False),   # Blocked user
    ]
    
    for user in users:
        db_session.add(user)
    db_session.commit()
    
    for user in users:
        db_session.refresh(user)
    print(f"✅ Created {len(users)} users")
    
    # Create Profiles
    profiles = [
        Profile(user_id=users[0].id, church_id=churches[0].id, nickname="admin_user", thumbnail="https://example.com/admin.jpg"),
        Profile(user_id=users[1].id, church_id=churches[0].id, nickname="john_doe", thumbnail="https://example.com/john.jpg"),
        Profile(user_id=users[2].id, church_id=churches[1].id, nickname="jane_smith", thumbnail="https://example.com/jane.jpg"),
        Profile(user_id=users[3].id, church_id=churches[2].id, nickname="bob_wilson"),
        Profile(user_id=users[4].id, church_id=churches[0].id, nickname="blocked_user"),
    ]
    
    for profile in profiles:
        db_session.add(profile)
    db_session.commit()
    
    for profile in profiles:
        db_session.refresh(profile)
    print(f"✅ Created {len(profiles)} profiles")
    
    # Create Boards
    boards = [
        Board(title="General Discussion", description="A place for general community discussions"),
        Board(title="Prayer Requests", description="Share your prayer requests with the community"),
        Board(title="Events & Announcements", description="Church events and important announcements"),
        Board(title="Bible Study", description="Discuss Bible passages and theological topics"),
    ]
    
    for board in boards:
        db_session.add(board)
    db_session.commit()
    
    for board in boards:
        db_session.refresh(board)
    print(f"✅ Created {len(boards)} boards")
    
    # Create Posts
    posts = [
        Post(
            board_id=boards[0].id,
            author_id=users[0].id,
            title="Welcome to Our Community!",
            contents="Hello everyone! Welcome to our church community platform. Feel free to introduce yourselves and share what's on your heart.",
            like_count=5,
            comment_count=2,
            view_count=25
        ),
        Post(
            board_id=boards[1].id,
            author_id=users[1].id,
            title="Prayer for Healing",
            contents="Please pray for my grandmother who is recovering from surgery. She's doing well but could use your prayers for a speedy recovery.",
            like_count=8,
            comment_count=3,
            view_count=15
        ),
        Post(
            board_id=boards[2].id,
            author_id=users[0].id,
            title="Youth Group Meeting - Saturday 7PM",
            contents="Don't forget about our youth group meeting this Saturday at 7PM in the fellowship hall. We'll be discussing the upcoming mission trip!",
            like_count=3,
            comment_count=1,
            view_count=20
        ),
        Post(
            board_id=boards[3].id,
            author_id=users[2].id,
            title="Thoughts on Romans 8:28",
            contents="I've been reflecting on Romans 8:28 lately. 'And we know that in all things God works for the good of those who love him...' What are your thoughts on this verse?",
            like_count=6,
            comment_count=4,
            view_count=30
        ),
    ]
    
    for post in posts:
        db_session.add(post)
    db_session.commit()
    
    for post in posts:
        db_session.refresh(post)
    print(f"✅ Created {len(posts)} posts")
    
    # Create Post Tags
    post_tags = [
        PostTag(post_id=posts[0].id, tag="welcome"),
        PostTag(post_id=posts[0].id, tag="introduction"),
        PostTag(post_id=posts[1].id, tag="prayer"),
        PostTag(post_id=posts[1].id, tag="healing"),
        PostTag(post_id=posts[2].id, tag="youth"),
        PostTag(post_id=posts[2].id, tag="events"),
        PostTag(post_id=posts[3].id, tag="bible-study"),
        PostTag(post_id=posts[3].id, tag="romans"),
    ]
    
    for tag in post_tags:
        db_session.add(tag)
    db_session.commit()
    print(f"✅ Created {len(post_tags)} post tags")
    
    # Create Comments
    comments = [
        Comment(post_id=posts[0].id, author_id=users[1].id, contents="Thank you for the warm welcome! Excited to be part of this community."),
        Comment(post_id=posts[0].id, author_id=users[2].id, contents="Looking forward to getting to know everyone better!"),
        Comment(post_id=posts[1].id, author_id=users[2].id, contents="Praying for your grandmother's quick recovery! 🙏"),
        Comment(post_id=posts[1].id, author_id=users[3].id, contents="Sending prayers and positive thoughts your way."),
        Comment(post_id=posts[1].id, author_id=users[0].id, contents="Our whole church family is praying for her healing."),
        Comment(post_id=posts[2].id, author_id=users[1].id, contents="I'll be there! Can't wait to hear about the mission trip details."),
        Comment(post_id=posts[3].id, author_id=users[1].id, contents="Such a powerful verse! It's been a source of comfort during difficult times."),
        Comment(post_id=posts[3].id, author_id=users[3].id, contents="I love how this verse reminds us that God has a plan even when we can't see it."),
    ]
    
    for comment in comments:
        db_session.add(comment)
    db_session.commit()
    
    for comment in comments:
        db_session.refresh(comment)
    print(f"✅ Created {len(comments)} comments")
    
    # Create Identity Verifications
    verifications = [
        IdentityVerification(
            user_id=users[1].id,
            church_id=churches[0].id,
            photo_url="https://example.com/verification/john_doe.jpg",
            status="approved",
            reviewed_by=users[0].id,
            reviewed_at=datetime.now() - timedelta(days=1)
        ),
        IdentityVerification(
            user_id=users[2].id,
            church_id=churches[1].id,
            photo_url="https://example.com/verification/jane_smith.jpg",
            status="pending"
        ),
        IdentityVerification(
            user_id=users[3].id,
            church_id=churches[2].id,
            photo_url="https://example.com/verification/bob_wilson.jpg",
            status="rejected",
            reviewed_by=users[0].id,
            reviewed_at=datetime.now() - timedelta(hours=2)
        ),
    ]
    
    for verification in verifications:
        db_session.add(verification)
    db_session.commit()
    
    for verification in verifications:
        db_session.refresh(verification)
    print(f"✅ Created {len(verifications)} identity verifications")
    
    # Create Action Logs
    actions = [
        ActionLog(user_id=users[1].id, action_type="like", target_type="post", target_id=posts[0].id, is_on=True),
        ActionLog(user_id=users[2].id, action_type="like", target_type="post", target_id=posts[0].id, is_on=True),
        ActionLog(user_id=users[3].id, action_type="like", target_type="post", target_id=posts[1].id, is_on=True),
        ActionLog(user_id=users[1].id, action_type="bookmark", target_type="post", target_id=posts[3].id, is_on=True),
        ActionLog(user_id=users[2].id, action_type="view", target_type="post", target_id=posts[2].id, is_on=True),
        ActionLog(user_id=users[1].id, action_type="like", target_type="comment", target_id=comments[0].id, is_on=True),
    ]
    
    for action in actions:
        db_session.add(action)
    db_session.commit()
    print(f"✅ Created {len(actions)} action logs")
    
    return {
        'churches': len(churches),
        'users': len(users),
        'profiles': len(profiles),
        'boards': len(boards),
        'posts': len(posts),
        'post_tags': len(post_tags),
        'comments': len(comments),
        'verifications': len(verifications),
        'actions': len(actions)
    }

def main():
    """Main function"""
    
    print("🏗️  GoChurch Sample Data Generator")
    print("=" * 50)
    
    # Parse command line arguments
    force_mode = '--force' in sys.argv or '-f' in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
Usage: python scripts/generate_sample_data.py [OPTIONS]

Options:
  --force, -f     Skip confirmation and generate data immediately
  --help, -h      Show this help message

This script generates comprehensive sample data including:
  - Churches with contact information
  - Users (admin, regular, and blocked)
  - User profiles with church associations
  - Discussion boards
  - Posts with engagement metrics
  - Comments and replies
  - Identity verification requests
  - User action logs (likes, bookmarks, views)

Examples:
  python scripts/generate_sample_data.py          # Interactive mode
  python scripts/generate_sample_data.py --force  # Skip confirmation
        """)
        return True
    
    if not force_mode:
        print("This will generate comprehensive sample data for testing.")
        response = input("\nProceed with sample data generation? (yes/no): ").lower().strip()
        
        if response not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            return False
    
    # Create database session
    db_session = SessionLocal()
    
    try:
        # Generate sample data
        stats = generate_sample_data(db_session)
        
        print(f"\n🎉 Sample data generation completed successfully!")
        print(f"📊 Summary:")
        for category, count in stats.items():
            print(f"   - {category.replace('_', ' ').title()}: {count}")
        
        total_records = sum(stats.values())
        print(f"   - Total records created: {total_records}")
        
        print(f"\n💡 Next steps:")
        print(f"   - Start the server: ./start.sh")
        print(f"   - Test the API: http://localhost:8000/docs")
        print(f"   - Clean up data: python scripts/remove_all_data.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error generating sample data: {str(e)}")
        db_session.rollback()
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db_session.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
