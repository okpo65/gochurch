#!/usr/bin/env python3
"""
Migration script to set up the new UUID-based database structure.
This script will create all tables according to the PostgreSQL schema provided.
"""

import sys
import os
from sqlalchemy import text

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, create_tables
from app.church.service import ChurchService
from app.church.schemas import ChurchCreate
from sqlalchemy.orm import sessionmaker

def enable_uuid_extension():
    """Enable UUID extension in PostgreSQL"""
    try:
        with engine.begin() as conn:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        print("✓ UUID extension enabled successfully")
        return True
    except Exception as e:
        print(f"Warning: Could not enable UUID extension: {e}")
        print("This might be okay if the extension is already enabled or if using a different UUID method")
        return False

def create_sample_data():
    """Create sample churches and data for testing"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create sample churches
        sample_churches = [
            {
                "name": "First Baptist Church",
                "address": "123 Main St, Anytown, USA",
                "phone_number": "+1-555-0123"
            },
            {
                "name": "Grace Community Church",
                "address": "456 Oak Ave, Somewhere, USA", 
                "phone_number": "+1-555-0456"
            },
            {
                "name": "New Life Fellowship",
                "address": "789 Pine Rd, Elsewhere, USA",
                "phone_number": "+1-555-0789"
            }
        ]
        
        for church_data in sample_churches:
            church = ChurchCreate(**church_data)
            ChurchService.create_church(db, church)
            print(f"✓ Created church: {church_data['name']}")
                
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def test_database_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    print("Starting migration to UUID-based schema...")
    print("=" * 50)
    
    # Test database connection first
    if not test_database_connection():
        print("Please check your database configuration in .env file")
        sys.exit(1)
    
    try:
        # Enable UUID extension
        print("1. Enabling UUID extension...")
        enable_uuid_extension()
        
        # Create all tables
        print("2. Creating database tables...")
        create_tables()
        
        # Create sample data
        print("3. Creating sample churches...")
        create_sample_data()
        
        print("\n" + "=" * 50)
        print("🎉 Migration completed successfully!")
        print("\nNew API Structure:")
        print("- Users: /users (UUID-based)")
        print("- Profiles: /users/profiles")
        print("- Churches: /churches")
        print("- Boards: /boards")
        print("- Posts: /boards/{board_id}/posts")
        print("- Comments: /boards/posts/{post_id}/comments")
        print("- Identity Verification: /verifications")
        print("- Action Logs: /actions")
        print("\nDocumentation:")
        print("- Swagger UI: http://localhost:8000/docs")
        print("- ReDoc: http://localhost:8000/redoc")
        print("\nNext steps:")
        print("1. Start the server: ./start.sh")
        print("2. Visit http://localhost:8000/docs to see the new API")
        print("3. All IDs are now UUIDs instead of integers")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if PostgreSQL is running")
        print("2. Verify database credentials in .env file")
        print("3. Ensure the database exists")
        print("4. Check if you have CREATE EXTENSION privileges")
        sys.exit(1)

if __name__ == "__main__":
    main()
