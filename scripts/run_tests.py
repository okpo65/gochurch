#!/usr/bin/env python3
"""
Test runner script for GoChurch Community Server
"""

import subprocess
import sys
import os

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

def main():
    """Main test runner"""
    print("🚀 GoChurch Community Server Test Suite")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if pytest is installed
    try:
        import pytest
        print("✅ pytest is available")
    except ImportError:
        print("❌ pytest is not installed. Installing...")
        if not run_command("pip install pytest pytest-asyncio", "Installing pytest"):
            sys.exit(1)
    
    # Check if faker is installed (needed for sample data)
    try:
        import faker
        print("✅ faker is available")
    except ImportError:
        print("❌ faker is not installed. Installing...")
        if not run_command("pip install faker", "Installing faker"):
            sys.exit(1)
    
    # Run different test suites
    test_commands = [
        ("pytest tests/test_users.py -v", "Running User API Tests"),
        ("pytest tests/test_churches.py -v", "Running Church API Tests"),
        ("pytest tests/test_community.py -v", "Running Community API Tests"),
        ("pytest tests/test_verification_actions.py -v", "Running Verification & Action Tests"),
        ("pytest tests/test_sample_data.py -v", "Running Sample Data Tests"),
    ]
    
    passed_tests = 0
    total_tests = len(test_commands)
    
    for command, description in test_commands:
        if run_command(command, description):
            passed_tests += 1
            print("✅ Test suite passed!")
        else:
            print("❌ Test suite failed!")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Passed: {passed_tests}/{total_tests}")
    print(f"Failed: {total_tests - passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
