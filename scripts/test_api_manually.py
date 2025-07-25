#!/usr/bin/env python3
"""
Manual API testing script
Tests all major endpoints with sample data
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, description=""):
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
            return None
        
        status_icon = "✅" if response.status_code < 400 else "❌"
        print(f"{status_icon} {method} {endpoint} - {response.status_code} - {description}")
        
        if response.status_code < 400:
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"   📊 Returned {len(data)} items")
                elif isinstance(data, dict) and 'id' in data:
                    print(f"   🆔 ID: {data['id']}")
                return data
            except:
                print(f"   📄 Response: {response.text[:100]}...")
                return response.text
        else:
            print(f"   ❌ Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {endpoint} - Connection Error: {e}")
        return None

def main():
    """Run comprehensive API tests"""
    print("🚀 GoChurch API Manual Testing")
    print("=" * 50)
    print(f"Testing server at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
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
    
    print("\n📋 Testing API Endpoints...")
    
    # Test Churches
    print("\n🏛️  CHURCH ENDPOINTS")
    churches = test_endpoint("GET", "/churches/", description="Get all churches")
    
    if churches and len(churches) > 0:
        church_id = churches[0]['id']
        test_endpoint("GET", f"/churches/{church_id}", description="Get specific church")
    
    # Test Users
    print("\n👥 USER ENDPOINTS")
    users = test_endpoint("GET", "/users/", description="Get all users")
    
    if users and len(users) > 0:
        user_id = users[0]['id']
        test_endpoint("GET", f"/users/{user_id}", description="Get specific user")
        
        # Test user profile
        profile = test_endpoint("GET", f"/users/{user_id}/profile", description="Get user profile")
    
    # Test Boards
    print("\n📋 BOARD ENDPOINTS")
    boards = test_endpoint("GET", "/boards/", description="Get all boards")
    
    if boards and len(boards) > 0:
        board_id = boards[0]['id']
        test_endpoint("GET", f"/boards/{board_id}", description="Get specific board")
        
        # Test posts in board
        posts = test_endpoint("GET", f"/boards/{board_id}/posts", description="Get posts in board")
        
        if posts and len(posts) > 0:
            post_id = posts[0]['id']
            test_endpoint("GET", f"/boards/posts/{post_id}", description="Get specific post")
            
            # Test comments on post
            comments = test_endpoint("GET", f"/boards/posts/{post_id}/comments", description="Get post comments")
            
            # Test post tags
            tags = test_endpoint("GET", f"/boards/posts/{post_id}/tags", description="Get post tags")
    
    # Test Verifications
    print("\n🔍 VERIFICATION ENDPOINTS")
    verifications = test_endpoint("GET", "/verifications/pending", description="Get pending verifications")
    all_verifications = test_endpoint("GET", "/verifications/status/pending", description="Get verifications by status")
    
    # Test Actions
    print("\n📊 ACTION LOG ENDPOINTS")
    if users and len(users) > 0:
        user_id = users[0]['id']
        user_actions = test_endpoint("GET", f"/actions/user/{user_id}", description="Get user actions")
    
    if posts and len(posts) > 0:
        post_id = posts[0]['id']
        post_actions = test_endpoint("GET", f"/actions/target/post/{post_id}", description="Get post actions")
        like_count = test_endpoint("GET", f"/actions/count/post/{post_id}/like", description="Get post like count")
    
    # Test Sample Data Generation
    print("\n🎲 DEVELOPMENT ENDPOINTS")
    test_endpoint("GET", "/tasks", description="Get all tasks")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 API TESTING SUMMARY")
    print("=" * 50)
    
    if churches:
        print(f"✅ Churches: {len(churches)} found")
    if users:
        print(f"✅ Users: {len(users)} found")
    if boards:
        print(f"✅ Boards: {len(boards)} found")
    if posts:
        print(f"✅ Posts: {len(posts)} found in first board")
    if comments:
        print(f"✅ Comments: {len(comments)} found in first post")
    
    print("\n🎯 Next Steps:")
    print("1. Visit Swagger docs: http://localhost:8000/docs")
    print("2. Try creating new data via API")
    print("3. Test authentication endpoints when implemented")
    print("4. Generate more sample data: curl -X POST http://localhost:8000/generate-sample-data")

if __name__ == "__main__":
    main()
