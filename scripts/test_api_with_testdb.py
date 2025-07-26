#!/usr/bin/env python3
"""
API testing script using test database with separate port
Tests all major endpoints with isolated test data
"""

import requests
import json
import sys
import os
import argparse
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import settings
from database import Base
from workers.tasks.sample_data import generate_all_sample_data

BASE_URL = "http://localhost:8000"

def get_test_database_url():
    """Generate test database URL with separate port"""
    return settings.get_test_database_url()

def get_postgres_url_for_test_db():
    """Get postgres database URL for test database server"""
    test_url = get_test_database_url()
    parts = test_url.rsplit("/", 1)
    return f"{parts[0]}/postgres"

def create_test_database_if_not_exists():
    """Create test database if it doesn't exist"""
    postgres_url = get_postgres_url_for_test_db()
    db_name = settings.TEST_DB_NAME
    
    try:
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            conn = conn.execution_options(autocommit=True)
            
            # Check if database exists
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

def setup_test_database():
    """Setup test database with sample data"""
    test_db_url = get_test_database_url()
    
    try:
        # Create test database if needed
        if not create_test_database_if_not_exists():
            return False
        
        # Create engine for test database
        engine = create_engine(test_db_url)
        
        # Enable UUID extension
        with engine.begin() as conn:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create session and generate sample data
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            print("🎲 Generating sample data in test database...")
            generate_all_sample_data(db)
            db.commit()
            print("✅ Sample data generated successfully")
        except Exception as e:
            db.rollback()
            print(f"❌ Error generating sample data: {e}")
            return False
        finally:
            db.close()
        
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Error setting up test database: {e}")
        return False

def cleanup_test_database():
    """Clean up test database"""
    test_db_url = get_test_database_url()
    
    try:
        engine = create_engine(test_db_url)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
        print(f"✅ Test database cleaned up on port {settings.TEST_DB_PORT}")
        return True
    except Exception as e:
        print(f"❌ Error cleaning up test database: {e}")
        return False

def drop_test_database():
    """Drop test database completely"""
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

def test_endpoint(method, endpoint, data=None, description="", expected_status=None):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return None, False
        
        # Check expected status
        if expected_status and response.status_code != expected_status:
            status_icon = "⚠️"
            success = False
        else:
            status_icon = "✅" if response.status_code < 400 else "❌"
            success = response.status_code < 400
        
        print(f"{status_icon} {method} {endpoint} - {response.status_code} - {description}")
        
        if response.status_code < 400:
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"   📊 Returned {len(data)} items")
                elif isinstance(data, dict) and 'id' in data:
                    print(f"   🆔 ID: {data['id']}")
                return data, success
            except:
                print(f"   📄 Response: {response.text[:100]}...")
                return response.text, success
        else:
            print(f"   ❌ Error: {response.text}")
            return None, success
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {endpoint} - Connection Error: {e}")
        return None, False

def run_comprehensive_api_tests():
    """Run comprehensive API tests"""
    print("🧪 Running Comprehensive API Tests")
    print("=" * 50)
    
    test_results = []
    
    # Test Churches
    print("\n🏛️  CHURCH ENDPOINTS")
    churches, success = test_endpoint("GET", "/churches/", description="Get all churches")
    test_results.append(("Churches List", success))
    
    if churches and len(churches) > 0:
        church_id = churches[0]['id']
        _, success = test_endpoint("GET", f"/churches/{church_id}", description="Get specific church")
        test_results.append(("Church Detail", success))
    
    # Test Users
    print("\n👥 USER ENDPOINTS")
    users, success = test_endpoint("GET", "/users/", description="Get all users")
    test_results.append(("Users List", success))
    
    if users and len(users) > 0:
        user_id = users[0]['id']
        _, success = test_endpoint("GET", f"/users/{user_id}", description="Get specific user")
        test_results.append(("User Detail", success))
        
        # Test user profile
        profile, success = test_endpoint("GET", f"/users/{user_id}/profile", description="Get user profile")
        test_results.append(("User Profile", success))
    
    # Test Boards
    print("\n📋 BOARD ENDPOINTS")
    boards, success = test_endpoint("GET", "/boards/", description="Get all boards")
    test_results.append(("Boards List", success))
    
    if boards and len(boards) > 0:
        board_id = boards[0]['id']
        _, success = test_endpoint("GET", f"/boards/{board_id}", description="Get specific board")
        test_results.append(("Board Detail", success))
        
        # Test posts in board
        posts, success = test_endpoint("GET", f"/boards/{board_id}/posts", description="Get posts in board")
        test_results.append(("Board Posts", success))
        
        if posts and len(posts) > 0:
            post_id = posts[0]['id']
            _, success = test_endpoint("GET", f"/boards/posts/{post_id}", description="Get specific post")
            test_results.append(("Post Detail", success))
            
            # Test comments on post
            comments, success = test_endpoint("GET", f"/boards/posts/{post_id}/comments", description="Get post comments")
            test_results.append(("Post Comments", success))
            
            # Test post tags
            tags, success = test_endpoint("GET", f"/boards/posts/{post_id}/tags", description="Get post tags")
            test_results.append(("Post Tags", success))
    
    # Test Verifications
    print("\n🔍 VERIFICATION ENDPOINTS")
    _, success = test_endpoint("GET", "/verifications/pending", description="Get pending verifications")
    test_results.append(("Pending Verifications", success))
    
    _, success = test_endpoint("GET", "/verifications/status/pending", description="Get verifications by status")
    test_results.append(("Verifications by Status", success))
    
    # Test Actions
    print("\n📊 ACTION LOG ENDPOINTS")
    if users and len(users) > 0:
        user_id = users[0]['id']
        _, success = test_endpoint("GET", f"/actions/user/{user_id}", description="Get user actions")
        test_results.append(("User Actions", success))
    
    if posts and len(posts) > 0:
        post_id = posts[0]['id']
        _, success = test_endpoint("GET", f"/actions/target/post/{post_id}", description="Get post actions")
        test_results.append(("Post Actions", success))
        
        _, success = test_endpoint("GET", f"/actions/count/post/{post_id}/like", description="Get post like count")
        test_results.append(("Post Like Count", success))
    
    # Test Development Endpoints
    print("\n🎲 DEVELOPMENT ENDPOINTS")
    _, success = test_endpoint("GET", "/tasks", description="Get all tasks")
    test_results.append(("Tasks List", success))
    
    return test_results

def print_test_summary(test_results):
    """Print test summary"""
    print("\n" + "=" * 60)
    print("📊 API TESTING SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if total - passed > 0:
        print("\n❌ Failed Tests:")
        for test_name, success in test_results:
            if not success:
                print(f"  - {test_name}")
    
    print(f"\n🎯 Database Configuration:")
    print(f"   Main DB: {settings.DATABASE_URL}")
    print(f"   Test DB: {get_test_database_url()}")
    print(f"   Main DB Port: {settings.DB_PORT}")
    print(f"   Test DB Port: {settings.TEST_DB_PORT}")
    print("\n🎯 Next Steps:")
    print("1. Visit Swagger docs: http://localhost:8000/docs")
    print("2. Run unit tests: python scripts/run_tests.py")
    print("3. Check test database for data integrity")

def main():
    """Main function with command line options"""
    parser = argparse.ArgumentParser(description="GoChurch API Testing with Separate Test Database")
    parser.add_argument("--setup-only", action="store_true", help="Only setup test database")
    parser.add_argument("--cleanup-only", action="store_true", help="Only cleanup test database")
    parser.add_argument("--drop-only", action="store_true", help="Only drop test database")
    parser.add_argument("--no-setup", action="store_true", help="Skip test database setup")
    parser.add_argument("--no-cleanup", action="store_true", help="Skip test database cleanup")
    
    args = parser.parse_args()
    
    print("🚀 GoChurch API Testing with Separate Test Database")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"Main Database: {settings.DATABASE_URL}")
    print(f"Test Database: {get_test_database_url()}")
    print(f"Main DB Port: {settings.DB_PORT}")
    print(f"Test DB Port: {settings.TEST_DB_PORT}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Handle setup-only
    if args.setup_only:
        if setup_test_database():
            print("✅ Test database setup completed")
        else:
            print("❌ Test database setup failed")
            sys.exit(1)
        return
    
    # Handle cleanup-only
    if args.cleanup_only:
        if cleanup_test_database():
            print("✅ Test database cleanup completed")
        else:
            print("❌ Test database cleanup failed")
            sys.exit(1)
        return
    
    # Handle drop-only
    if args.drop_only:
        if drop_test_database():
            print("✅ Test database dropped successfully")
        else:
            print("❌ Test database drop failed")
            sys.exit(1)
        return
    
    # Setup test database
    if not args.no_setup:
        print("🔧 Setting up test database...")
        if not setup_test_database():
            print("❌ Failed to setup test database")
            print(f"   Make sure PostgreSQL is running on port {settings.TEST_DB_PORT}")
            sys.exit(1)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            server_info = response.json()
            print(f"   Version: {server_info.get('version', 'Unknown')}")
            print(f"   Environment: {server_info.get('environment', 'Unknown')}")
        else:
            print("❌ Server responded with error")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Server is not running!")
        print("Please start the server with: ./start.sh")
        sys.exit(1)
    
    # Run API tests
    test_results = run_comprehensive_api_tests()
    
    # Print summary
    print_test_summary(test_results)
    
    # Cleanup test database
    if not args.no_cleanup:
        print("\n🧹 Cleaning up test database...")
        cleanup_test_database()
    
    # Exit with appropriate code
    failed_tests = sum(1 for _, success in test_results if not success)
    if failed_tests > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
