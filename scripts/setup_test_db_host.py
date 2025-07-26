#!/usr/bin/env python3
"""
Test Database Hosting Setup Script
Sets up a separate PostgreSQL instance for testing on port 5433
"""

import subprocess
import sys
import os
import argparse
import shutil
from pathlib import Path

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import settings

def run_command(command, description, check=True, capture_output=True):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"🔧 {description}")
    print(f"{'='*50}")
    print(f"Running: {command}")
    
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr and result.returncode == 0:
                print("STDERR:", result.stderr)
        else:
            result = subprocess.run(command, shell=True, check=check)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if capture_output:
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
        return False

def check_postgresql():
    """Check if PostgreSQL is installed"""
    commands = ['psql', 'initdb', 'pg_ctl', 'createdb', 'createuser']
    missing = []
    
    for cmd in commands:
        if not shutil.which(cmd):
            missing.append(cmd)
    
    if missing:
        print(f"❌ Missing PostgreSQL commands: {', '.join(missing)}")
        print("\n💡 Install PostgreSQL:")
        print("   macOS: brew install postgresql")
        print("   Ubuntu: sudo apt-get install postgresql postgresql-contrib")
        print("   CentOS: sudo yum install postgresql postgresql-server")
        return False
    
    print("✅ PostgreSQL commands available")
    return True

def get_test_db_data_dir():
    """Get test database data directory"""
    home = Path.home()
    return home / "postgres_test_data"

def init_test_database():
    """Initialize test database cluster"""
    data_dir = get_test_db_data_dir()
    
    if data_dir.exists():
        print(f"✅ Test database directory already exists: {data_dir}")
        return True
    
    print(f"🔧 Creating test database directory: {data_dir}")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize database cluster
    cmd = f'initdb -D "{data_dir}" -U {settings.TEST_DB_USER}'
    if not run_command(cmd, "Initializing test database cluster"):
        return False
    
    print("✅ Test database cluster initialized")
    return True

def start_test_database():
    """Start test PostgreSQL instance"""
    data_dir = get_test_db_data_dir()
    
    if not data_dir.exists():
        print("❌ Test database not initialized. Run with --init first.")
        return False
    
    # Check if already running
    if is_test_database_running():
        print(f"✅ Test database already running on port {settings.TEST_DB_PORT}")
        return True
    
    # Start PostgreSQL
    cmd = f'pg_ctl -D "{data_dir}" -o "-p {settings.TEST_DB_PORT}" start'
    if not run_command(cmd, f"Starting test database on port {settings.TEST_DB_PORT}"):
        return False
    
    print(f"✅ Test database started on port {settings.TEST_DB_PORT}")
    return True

def stop_test_database():
    """Stop test PostgreSQL instance"""
    data_dir = get_test_db_data_dir()
    
    if not data_dir.exists():
        print("⚠️  Test database directory doesn't exist")
        return True
    
    # Stop PostgreSQL
    cmd = f'pg_ctl -D "{data_dir}" stop'
    if not run_command(cmd, "Stopping test database", check=False):
        print("⚠️  Test database may not have been running")
    
    print("✅ Test database stopped")
    return True

def is_test_database_running():
    """Check if test database is running"""
    data_dir = get_test_db_data_dir()
    
    if not data_dir.exists():
        return False
    
    # Check status
    cmd = f'pg_ctl -D "{data_dir}" status'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

def create_test_user_and_database():
    """Create test user and database"""
    # Create user (if not exists)
    cmd = f'createuser -h {settings.TEST_DB_HOST} -p {settings.TEST_DB_PORT} -s {settings.TEST_DB_USER}'
    run_command(cmd, f"Creating test user: {settings.TEST_DB_USER}", check=False)
    
    # Create database (if not exists)
    cmd = f'createdb -h {settings.TEST_DB_HOST} -p {settings.TEST_DB_PORT} -O {settings.TEST_DB_USER} {settings.TEST_DB_NAME}'
    if run_command(cmd, f"Creating test database: {settings.TEST_DB_NAME}", check=False):
        print(f"✅ Test database created: {settings.TEST_DB_NAME}")
    else:
        print(f"⚠️  Test database may already exist: {settings.TEST_DB_NAME}")
    
    return True

def test_connection():
    """Test connection to test database"""
    cmd = f'psql -h {settings.TEST_DB_HOST} -p {settings.TEST_DB_PORT} -U {settings.TEST_DB_USER} -d {settings.TEST_DB_NAME} -c "SELECT version();"'
    if run_command(cmd, "Testing database connection"):
        print("✅ Test database connection successful")
        return True
    else:
        print("❌ Test database connection failed")
        return False

def show_status():
    """Show test database status"""
    print("🔍 Test Database Status")
    print("=" * 50)
    
    data_dir = get_test_db_data_dir()
    print(f"Data Directory: {data_dir}")
    print(f"Exists: {'✅' if data_dir.exists() else '❌'}")
    
    if data_dir.exists():
        running = is_test_database_running()
        print(f"Running: {'✅' if running else '❌'}")
        
        if running:
            print(f"Host: {settings.TEST_DB_HOST}")
            print(f"Port: {settings.TEST_DB_PORT}")
            print(f"Database: {settings.TEST_DB_NAME}")
            print(f"User: {settings.TEST_DB_USER}")
            
            # Test connection
            test_connection()

def cleanup_test_database():
    """Remove test database completely"""
    print("⚠️  This will completely remove the test database!")
    response = input("Are you sure? (yes/no): ").lower().strip()
    
    if response != 'yes':
        print("❌ Cancelled")
        return False
    
    # Stop database first
    stop_test_database()
    
    # Remove data directory
    data_dir = get_test_db_data_dir()
    if data_dir.exists():
        import shutil
        shutil.rmtree(data_dir)
        print(f"✅ Removed test database directory: {data_dir}")
    
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test Database Hosting Setup")
    parser.add_argument("action", choices=[
        "init", "start", "stop", "restart", "status", "cleanup", "setup", "test"
    ], help="Action to perform")
    
    args = parser.parse_args()
    
    print("🗄️  Test Database Hosting Setup")
    print("=" * 60)
    print(f"Project Root: {project_root}")
    print(f"Test DB Host: {settings.TEST_DB_HOST}")
    print(f"Test DB Port: {settings.TEST_DB_PORT}")
    print(f"Test DB Name: {settings.TEST_DB_NAME}")
    print(f"Test DB User: {settings.TEST_DB_USER}")
    print(f"Data Directory: {get_test_db_data_dir()}")
    print("=" * 60)
    
    # Check PostgreSQL installation
    if not check_postgresql():
        sys.exit(1)
    
    success = True
    
    if args.action == "init":
        success = init_test_database()
    
    elif args.action == "start":
        success = start_test_database()
    
    elif args.action == "stop":
        success = stop_test_database()
    
    elif args.action == "restart":
        stop_test_database()
        success = start_test_database()
    
    elif args.action == "status":
        show_status()
    
    elif args.action == "cleanup":
        success = cleanup_test_database()
    
    elif args.action == "setup":
        # Complete setup process
        success = (
            init_test_database() and
            start_test_database() and
            create_test_user_and_database() and
            test_connection()
        )
        
        if success:
            print("\n🎉 Test database setup completed successfully!")
            print("\n📋 Next steps:")
            print("1. Run tests: poetry run python scripts/run_tests.py")
            print("2. Stop test DB when done: python scripts/setup_test_db_host.py stop")
        else:
            print("\n❌ Test database setup failed!")
    
    elif args.action == "test":
        success = test_connection()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
