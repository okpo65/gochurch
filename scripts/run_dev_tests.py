#!/usr/bin/env python3
"""
Development test runner that uses the main database
This allows you to test APIs with persistent sample data
"""

import subprocess
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"🧪 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def check_database_connection():
    """Check if we can connect to the main database"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def generate_sample_data():
    """Generate sample data in the main database"""
    try:
        from tasks.sample_data import generate_all_sample_data
        print("🚀 Generating sample data in main database...")
        result = generate_all_sample_data()
        print("✅ Sample data generated successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to generate sample data: {e}")
        return False

def run_api_tests_against_main_db():
    """Run API tests against the main database with sample data"""
    
    # Temporarily modify the test configuration to use main DB
    test_commands = [
        'python -c "import requests; r=requests.get(\'http://localhost:8000/users/\'); print(f\'Users: {len(r.json())} found\')"',
        'python -c "import requests; r=requests.get(\'http://localhost:8000/churches/\'); print(f\'Churches: {len(r.json())} found\')"',
        'python -c "import requests; r=requests.get(\'http://localhost:8000/boards/\'); print(f\'Boards: {len(r.json())} found\')"',
    ]
    
    print("\n🔍 Testing API endpoints with sample data...")
    
    for command in test_commands:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {result.stdout.strip()}")
            else:
                print(f"❌ API test failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Error running API test: {e}")

def main():
    """Main development test runner"""
    print("🚀 GoChurch Development Test Runner")
    print("This runner uses your MAIN database and generates persistent sample data")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check database connection
    if not check_database_connection():
        print("Please check your database configuration and ensure the server is running")
        sys.exit(1)
    
    # Ask user for confirmation
    print("\n⚠️  WARNING: This will add sample data to your MAIN database")
    print("   Database:", settings.DATABASE_URL)
    response = input("\nDo you want to continue? (y/N): ").lower().strip()
    
    if response != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    
    # Generate sample data
    if not generate_sample_data():
        sys.exit(1)
    
    # Check if server is running
    try:
        import requests
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            run_api_tests_against_main_db()
        else:
            print("⚠️  Server responded but with error status")
    except requests.exceptions.RequestException:
        print("⚠️  Server is not running. Start it with: ./start.sh")
        print("   Then you can test the API manually:")
        print("   curl http://localhost:8000/users/")
        print("   curl http://localhost:8000/boards/")
        print("   curl http://localhost:8000/churches/")
    
    print(f"\n{'='*70}")
    print("🎉 Development setup complete!")
    print("=" * 70)
    print("Your main database now contains sample data for testing.")
    print("\nNext steps:")
    print("1. Start the server: ./start.sh")
    print("2. Visit Swagger docs: http://localhost:8000/docs")
    print("3. Test API endpoints manually")
    print("4. Clean up when done: curl -X POST http://localhost:8000/cleanup-data")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
