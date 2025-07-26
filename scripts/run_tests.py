#!/usr/bin/env python3
"""
Enhanced test runner script for GoChurch Community Server
Supports test database management with separate ports for isolation
"""

import subprocess
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

def get_test_database_url():
    """Generate test database URL with separate port"""
    return settings.get_test_database_url()

def get_postgres_url_for_test_db():
    """Get postgres database URL for test database server"""
    test_url = get_test_database_url()
    parts = test_url.rsplit("/", 1)
    return f"{parts[0]}/postgres"

def run_command(command, description, capture_output=True):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"🧪 {description}")
    print(f"{'='*50}")
    
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
        else:
            result = subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if capture_output:
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
        return False

def create_test_database():
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
        print(f"   Main DB Port: {settings.DB_PORT}")
        print(f"   Test DB Port: {settings.TEST_DB_PORT}")
        return False

def drop_test_database():
    """Drop test database"""
    postgres_url = get_postgres_url_for_test_db()
    db_name = settings.TEST_DB_NAME
    
    try:
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            conn = conn.execution_options(autocommit=True)
            
            # Terminate connections to the test database
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

def check_dependencies():
    """Check if required dependencies are installed"""
    dependencies = [
        ("pytest", "pytest pytest-asyncio"),
        ("faker", "faker"),
        ("requests", "requests")
    ]
    
    for module, install_cmd in dependencies:
        try:
            __import__(module)
            print(f"✅ {module} is available")
        except ImportError:
            print(f"❌ {module} is not installed. Installing...")
            if not run_command(f"pip install {install_cmd}", f"Installing {module}"):
                return False
    
    return True

def check_database_connectivity():
    """Check if both main and test databases are accessible"""
    print(f"🔍 Checking database connectivity...")
    print(f"   Main DB: {settings.DATABASE_URL}")
    print(f"   Test DB: {get_test_database_url()}")
    
    # Check main database
    try:
        main_engine = create_engine(settings.DATABASE_URL)
        with main_engine.connect():
            print(f"✅ Main database accessible on port {settings.DB_PORT}")
        main_engine.dispose()
    except Exception as e:
        print(f"⚠️  Main database connection issue: {e}")
    
    # Check test database server
    try:
        postgres_url = get_postgres_url_for_test_db()
        test_engine = create_engine(postgres_url)
        with test_engine.connect():
            print(f"✅ Test database server accessible on port {settings.TEST_DB_PORT}")
        test_engine.dispose()
    except Exception as e:
        print(f"❌ Test database server not accessible: {e}")
        print(f"   Please ensure PostgreSQL is running on port {settings.TEST_DB_PORT}")
        return False
    
    return True

def run_tests(test_pattern=None, verbose=False, coverage=False, parallel=False):
    """Run tests with various options"""
    
    # Set PYTHONPATH for the test subprocess
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root
    
    # Base pytest command
    cmd_parts = ["pytest"]
    
    if verbose:
        cmd_parts.append("-v")
    
    if coverage:
        cmd_parts.extend(["--cov=app", "--cov-report=html", "--cov-report=term"])
    
    if parallel:
        cmd_parts.extend(["-n", "auto"])
    
    if test_pattern:
        cmd_parts.append(test_pattern)
    else:
        cmd_parts.append("tests/")
    
    command = " ".join(cmd_parts)
    
    try:
        result = subprocess.run(command, shell=True, check=True, env=env)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False

def main():
    """Main test runner with command line options"""
    parser = argparse.ArgumentParser(description="GoChurch Test Runner with Separate Database Ports")
    parser.add_argument("--pattern", "-p", help="Test pattern to run (e.g., tests/test_users.py)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Run with coverage")
    parser.add_argument("--parallel", "-j", action="store_true", help="Run tests in parallel")
    parser.add_argument("--create-db", action="store_true", help="Create test database")
    parser.add_argument("--drop-db", action="store_true", help="Drop test database")
    parser.add_argument("--reset-db", action="store_true", help="Reset test database")
    parser.add_argument("--no-db-setup", action="store_true", help="Skip database setup")
    parser.add_argument("--check-db", action="store_true", help="Check database connectivity")
    
    args = parser.parse_args()
    
    print("🚀 GoChurch Community Server Test Suite")
    print("=" * 60)
    print(f"Project Root: {project_root}")
    print(f"Main Database: {settings.DATABASE_URL}")
    print(f"Test Database: {get_test_database_url()}")
    print(f"Main DB Port: {settings.DB_PORT}")
    print(f"Test DB Port: {settings.TEST_DB_PORT}")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists(os.path.join(project_root, "main.py")):
        print("❌ Error: main.py not found in project root")
        print(f"   Expected: {os.path.join(project_root, 'main.py')}")
        sys.exit(1)
    
    # Check database connectivity
    if args.check_db or not args.no_db_setup:
        if not check_database_connectivity():
            print("\n💡 Setup Instructions:")
            print(f"   1. Make sure PostgreSQL is running on port {settings.TEST_DB_PORT}")
            print(f"   2. You can start a separate PostgreSQL instance for testing:")
            print(f"      pg_ctl -D /path/to/test/data -o '-p {settings.TEST_DB_PORT}' start")
            print(f"   3. Or configure TEST_DB_PORT in your .env file to use the same port as main DB")
            if not args.check_db:
                sys.exit(1)
    
    if args.check_db:
        return
    
    # Handle database operations
    if args.drop_db or args.reset_db:
        if not drop_test_database():
            sys.exit(1)
    
    if args.create_db or args.reset_db or not args.no_db_setup:
        if not create_test_database():
            sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run tests
    if not (args.create_db or args.drop_db):
        success = run_tests(
            test_pattern=args.pattern,
            verbose=args.verbose,
            coverage=args.coverage,
            parallel=args.parallel
        )
        
        if success:
            print("\n🎉 All tests completed successfully!")
            if args.coverage:
                print("📊 Coverage report generated in htmlcov/index.html")
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)

if __name__ == "__main__":
    main()
