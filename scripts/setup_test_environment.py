#!/usr/bin/env python3
"""
Comprehensive Test Environment Setup Script
Sets up everything needed for testing including test database hosting
"""

import subprocess
import sys
import os
import argparse
import time

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import settings

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"🔧 {description}")
    print(f"{'='*50}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode == 0:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def setup_test_database_host():
    """Setup test database hosting"""
    print("🗄️  Setting up test database hosting...")
    
    # Use the test database hosting script
    script_path = os.path.join(project_root, "scripts", "setup_test_db_host.py")
    cmd = f"python {script_path} setup"
    
    return run_command(cmd, "Setting up test database host")

def run_tests():
    """Run the test suite"""
    print("🧪 Running test suite...")
    
    script_path = os.path.join(project_root, "scripts", "run_tests.py")
    cmd = f"python {script_path} --verbose"
    
    return run_command(cmd, "Running tests", check=False)

def run_api_tests():
    """Run API tests"""
    print("🌐 Running API tests...")
    
    script_path = os.path.join(project_root, "scripts", "test_api_with_testdb.py")
    cmd = f"python {script_path}"
    
    return run_command(cmd, "Running API tests", check=False)

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    # Check .env file
    env_file = os.path.join(project_root, ".env")
    if not os.path.exists(env_file):
        print("❌ .env file not found")
        return False
    
    print("✅ .env file exists")
    
    # Check required environment variables
    required_vars = [
        'DATABASE_URL', 'TEST_DB_HOST', 'TEST_DB_PORT', 
        'TEST_DB_NAME', 'TEST_DB_USER'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not hasattr(settings, var) or not getattr(settings, var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment variables configured")
    
    # Display configuration
    print(f"\n📊 Configuration:")
    print(f"   Main DB: {settings.DATABASE_URL}")
    print(f"   Test DB: {settings.get_test_database_url()}")
    print(f"   Main DB Port: {settings.DB_PORT}")
    print(f"   Test DB Port: {settings.TEST_DB_PORT}")
    
    return True

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description="Comprehensive Test Environment Setup")
    parser.add_argument("--skip-db-setup", action="store_true", help="Skip test database setup")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-api-tests", action="store_true", help="Skip API tests")
    parser.add_argument("--setup-only", action="store_true", help="Only setup, don't run tests")
    
    args = parser.parse_args()
    
    print("🚀 GoChurch Comprehensive Test Environment Setup")
    print("=" * 70)
    print(f"Project Root: {project_root}")
    print("=" * 70)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed!")
        print("\n💡 Make sure your .env file is properly configured")
        sys.exit(1)
    
    success_steps = []
    failed_steps = []
    
    # Setup test database hosting
    if not args.skip_db_setup:
        print("\n" + "="*70)
        print("STEP 1: Setting up test database hosting")
        print("="*70)
        
        if setup_test_database_host():
            success_steps.append("Test database hosting setup")
            print("✅ Test database hosting setup completed")
        else:
            failed_steps.append("Test database hosting setup")
            print("❌ Test database hosting setup failed")
    
    # Wait a moment for database to be ready
    if not args.skip_db_setup:
        print("\n⏳ Waiting for database to be ready...")
        time.sleep(2)
    
    # Run unit tests
    if not args.skip_tests and not args.setup_only:
        print("\n" + "="*70)
        print("STEP 2: Running unit tests")
        print("="*70)
        
        if run_tests():
            success_steps.append("Unit tests")
            print("✅ Unit tests completed successfully")
        else:
            failed_steps.append("Unit tests")
            print("❌ Some unit tests failed")
    
    # Run API tests
    if not args.skip_api_tests and not args.setup_only:
        print("\n" + "="*70)
        print("STEP 3: Running API tests")
        print("="*70)
        
        if run_api_tests():
            success_steps.append("API tests")
            print("✅ API tests completed successfully")
        else:
            failed_steps.append("API tests")
            print("❌ Some API tests failed")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SETUP SUMMARY")
    print("="*70)
    
    if success_steps:
        print("✅ Successful steps:")
        for step in success_steps:
            print(f"   - {step}")
    
    if failed_steps:
        print("\n❌ Failed steps:")
        for step in failed_steps:
            print(f"   - {step}")
    
    print(f"\nTotal: {len(success_steps)} successful, {len(failed_steps)} failed")
    
    if not failed_steps:
        print("\n🎉 All setup completed successfully!")
        print("\n📋 Your test environment is ready!")
        print("\n🎯 Next steps:")
        print("   1. Run tests anytime: poetry run python scripts/run_tests.py")
        print("   2. Run API tests: poetry run python scripts/test_api_with_testdb.py")
        print("   3. Stop test DB when done: python scripts/setup_test_db_host.py stop")
        print("   4. Start main server: ./start.sh")
    else:
        print("\n⚠️  Some steps failed, but you can still proceed")
        print("\n🔧 Troubleshooting:")
        print("   1. Check PostgreSQL installation: brew install postgresql")
        print("   2. Check .env configuration")
        print("   3. Run individual setup steps manually")
        sys.exit(1)

if __name__ == "__main__":
    main()
