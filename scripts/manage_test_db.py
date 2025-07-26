#!/usr/bin/env python3
"""
Test database management script with separate port support
"""

import sys
import os
import argparse

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now we can import project modules
from sqlalchemy import create_engine, text
from config.config import settings
from database import Base

def get_test_database_url():
    """Generate test database URL with separate port"""
    return settings.get_test_database_url()

def get_postgres_url_for_test_db():
    """Get postgres database URL for test database server"""
    test_url = get_test_database_url()
    parts = test_url.rsplit("/", 1)
    return f"{parts[0]}/postgres"

def create_test_database():
    """Create test database"""
    postgres_url = get_postgres_url_for_test_db()
    db_name = settings.TEST_DB_NAME
    
    try:
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            conn = conn.execution_options(autocommit=True)
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            if not result.fetchone():
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                print(f"✅ Created test database: {db_name} on port {settings.TEST_DB_PORT}")
            else:
                print(f"✅ Test database already exists: {db_name} on port {settings.TEST_DB_PORT}")
        engine.dispose()
        return True
    except Exception as e:
        print(f"❌ Failed to create test database: {e}")
        print(f"   Make sure PostgreSQL is running on port {settings.TEST_DB_PORT}")
        return False

def setup_test_tables():
    """Setup test database tables"""
    test_db_url = get_test_database_url()
    
    try:
        engine = create_engine(test_db_url)
        
        # Enable UUID extension
        with engine.begin() as conn:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print(f"✅ Test database tables created on port {settings.TEST_DB_PORT}")
        
        engine.dispose()
        return True
    except Exception as e:
        print(f"❌ Failed to setup test tables: {e}")
        return False

def drop_test_database():
    """Drop test database"""
    postgres_url = get_postgres_url_for_test_db()
    db_name = settings.TEST_DB_NAME
    
    try:
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            conn = conn.execution_options(autocommit=True)
            
            # Terminate connections
            conn.execute(text(f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = '{db_name}' AND pid <> pg_backend_pid()
            """))
            
            # Drop database
            conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))
            print(f"✅ Dropped test database: {db_name} from port {settings.TEST_DB_PORT}")
        
        engine.dispose()
        return True
    except Exception as e:
        print(f"❌ Failed to drop test database: {e}")
        return False

def check_connectivity():
    """Check database connectivity"""
    print("🔍 Checking database connectivity...")
    
    # Check main database
    try:
        main_engine = create_engine(settings.DATABASE_URL)
        with main_engine.connect():
            print(f"✅ Main database accessible: {settings.DATABASE_URL}")
        main_engine.dispose()
    except Exception as e:
        print(f"❌ Main database connection failed: {e}")
    
    # Check test database server
    try:
        postgres_url = get_postgres_url_for_test_db()
        test_engine = create_engine(postgres_url)
        with test_engine.connect():
            print(f"✅ Test database server accessible on port {settings.TEST_DB_PORT}")
        test_engine.dispose()
    except Exception as e:
        print(f"❌ Test database server connection failed: {e}")
        print(f"   Make sure PostgreSQL is running on port {settings.TEST_DB_PORT}")
        return False
    
    # Check if test database exists
    try:
        test_db_url = get_test_database_url()
        test_db_engine = create_engine(test_db_url)
        with test_db_engine.connect():
            print(f"✅ Test database accessible: {settings.TEST_DB_NAME}")
        test_db_engine.dispose()
    except Exception as e:
        print(f"⚠️  Test database not accessible (may not exist): {e}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Test Database Management with Separate Ports")
    parser.add_argument("action", choices=["create", "setup", "drop", "reset", "info", "check"])
    
    args = parser.parse_args()
    
    print("🗄️  Test Database Management")
    print("=" * 50)
    print(f"Project Root: {project_root}")
    print(f"Main Database: {settings.DATABASE_URL}")
    print(f"Test Database: {get_test_database_url()}")
    print(f"Main DB Port: {settings.DB_PORT}")
    print(f"Test DB Port: {settings.TEST_DB_PORT}")
    print("=" * 50)
    
    if args.action == "create":
        create_test_database()
    elif args.action == "setup":
        if create_test_database():
            setup_test_tables()
    elif args.action == "drop":
        drop_test_database()
    elif args.action == "reset":
        drop_test_database()
        if create_test_database():
            setup_test_tables()
    elif args.action == "check":
        check_connectivity()
    elif args.action == "info":
        print(f"\n📊 Database Configuration:")
        print(f"   Main DB Host: {settings.DB_HOST}")
        print(f"   Main DB Port: {settings.DB_PORT}")
        print(f"   Main DB Name: {settings.DB_NAME}")
        print(f"   Main DB User: {settings.DB_USER}")
        print(f"   Test DB Host: {settings.TEST_DB_HOST}")
        print(f"   Test DB Port: {settings.TEST_DB_PORT}")
        print(f"   Test DB Name: {settings.TEST_DB_NAME}")
        print(f"   Test DB User: {settings.TEST_DB_USER}")
        print(f"\n🔗 Connection URLs:")
        print(f"   Main: {settings.DATABASE_URL}")
        print(f"   Test: {get_test_database_url()}")

if __name__ == "__main__":
    main()
