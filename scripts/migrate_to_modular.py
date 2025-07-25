#!/usr/bin/env python3
"""
Migration script to set up the new modular database structure.
Run this after updating the code to create all necessary tables.
"""

import sys
import os
from sqlalchemy import text

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, create_tables
from app.settings.service import SystemSettingsService, NotificationSettingsService
from app.settings.schemas import SystemSettingsCreate
from sqlalchemy.orm import sessionmaker

def create_default_system_settings():
    """Create default system settings"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        default_settings = [
            {
                "key": "site_name",
                "value": "GoChurch Community",
                "description": "Name of the community site",
                "category": "general",
                "is_public": True
            },
            {
                "key": "site_description", 
                "value": "A community platform for church members",
                "description": "Description of the community site",
                "category": "general",
                "is_public": True
            },
            {
                "key": "max_file_size",
                "value": "10485760",  # 10MB in bytes
                "description": "Maximum file upload size in bytes",
                "category": "uploads",
                "is_public": False
            },
            {
                "key": "allowed_file_types",
                "value": "jpg,jpeg,png,gif,pdf,doc,docx",
                "description": "Allowed file extensions for uploads",
                "category": "uploads", 
                "is_public": False
            },
            {
                "key": "registration_enabled",
                "value": "true",
                "description": "Whether new user registration is enabled",
                "category": "auth",
                "is_public": True
            },
            {
                "key": "email_verification_required",
                "value": "false",
                "description": "Whether email verification is required for new users",
                "category": "auth",
                "is_public": False
            }
        ]
        
        for setting_data in default_settings:
            # Check if setting already exists
            existing = SystemSettingsService.get_system_setting(db, setting_data["key"])
            if not existing:
                setting = SystemSettingsCreate(**setting_data)
                SystemSettingsService.create_system_setting(db, setting)
                print(f"Created system setting: {setting_data['key']}")
            else:
                print(f"System setting already exists: {setting_data['key']}")
                
    except Exception as e:
        print(f"Error creating system settings: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("Starting migration to modular structure...")
    
    try:
        # Create all tables
        print("Creating database tables...")
        create_tables()
        print("✓ Database tables created successfully")
        
        # Create default system settings
        print("Creating default system settings...")
        create_default_system_settings()
        print("✓ Default system settings created")
        
        print("\n🎉 Migration completed successfully!")
        print("\nNext steps:")
        print("1. Install new dependencies: poetry install")
        print("2. Start the server: ./start.sh")
        print("3. Visit http://localhost:8000/docs to see the new API")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
