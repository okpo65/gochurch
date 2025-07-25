# GoChurch Community Server - Testing & Sample Data Guide

## 🤔 **Understanding the Testing Options**

You have **3 different ways** to test your API, each serving different purposes:

### **Option 1: Isolated Unit Tests** 
```bash
python run_tests.py
```
- **Database**: Uses `test_fastapi_celery_db` (separate from your main data)
- **Purpose**: Automated testing, CI/CD, development validation
- **Data**: Temporary - created and destroyed for each test
- **Manual API Testing**: ❌ No - data is cleaned up immediately

### **Option 2: Development Testing with Persistent Data**
```bash
python run_dev_tests.py
```
- **Database**: Uses your main `fastapi_celery_db` 
- **Purpose**: Generate sample data for manual API testing
- **Data**: Persistent - stays in your database for manual testing
- **Manual API Testing**: ✅ Yes - perfect for this!

### **Option 3: Manual API Testing**
```bash
python test_api_manually.py
```
- **Database**: Uses whatever data is currently in your main database
- **Purpose**: Test all API endpoints manually with existing data
- **Data**: Uses existing data (run Option 2 first to populate)
- **Manual API Testing**: ✅ Yes - comprehensive endpoint testing

## 📊 **Database Usage Comparison**

| Method | Database Used | Data Persistence | Manual API Testing | Purpose |
|--------|---------------|------------------|-------------------|---------|
| `run_tests.py` | `test_fastapi_celery_db` | Temporary | ❌ No | Unit testing |
| `run_dev_tests.py` | `fastapi_celery_db` | Persistent | ✅ Yes | Development |
| `test_api_manually.py` | `fastapi_celery_db` | Uses existing | ✅ Yes | Manual testing |
| API endpoints | `fastapi_celery_db` | Persistent | ✅ Yes | Production-like |

## 🎯 **Recommended Workflow**

### **For Development & Manual API Testing:**
```bash
# 1. Generate sample data in your main database
python run_dev_tests.py

# 2. Start your server
./start.sh

# 3. Test API endpoints manually
python test_api_manually.py

# 4. Or use Swagger UI
open http://localhost:8000/docs

# 5. Clean up when done (optional)
curl -X POST "http://localhost:8000/cleanup-data"
```

### **For Automated Testing:**
```bash
# Run isolated unit tests (won't affect your main data)
python run_tests.py
```

### **For Quick Sample Data Generation:**
```bash
# Start server first
./start.sh

# Generate sample data via API
curl -X POST "http://localhost:8000/generate-sample-data"

# Check task status
curl "http://localhost:8000/task/{task_id}"
```

## 🧪 Testing Overview

This project includes comprehensive API tests and sample data generation to help you develop and test the GoChurch Community Server.

## 📁 Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Test configuration and fixtures
├── test_users.py                  # User and profile API tests
├── test_churches.py               # Church management API tests
├── test_community.py              # Board, post, and comment tests
├── test_verification_actions.py   # Verification and action log tests
└── test_sample_data.py           # Sample data generation tests
```

## 🚀 Running Tests

### **Quick Test Run**
```bash
# Run all tests (isolated test database)
python run_tests.py

# Or use pytest directly
pytest tests/ -v
```

### **Run Specific Test Suites**
```bash
# User tests
pytest tests/test_users.py -v

# Church tests
pytest tests/test_churches.py -v

# Community tests (boards, posts, comments)
pytest tests/test_community.py -v

# Verification and action tests
pytest tests/test_verification_actions.py -v

# Sample data tests
pytest tests/test_sample_data.py -v
```

### **Run Individual Tests**
```bash
# Run a specific test
pytest tests/test_users.py::TestUsers::test_create_user -v

# Run tests with keyword matching
pytest tests/ -k "create_user" -v
```

## 📊 Sample Data Generation

### **Generate Sample Data via API**
```bash
# Start the server
./start.sh

# Generate sample data (returns task ID)
curl -X POST "http://localhost:8000/generate-sample-data"

# Check task status
curl "http://localhost:8000/task/{task_id}"

# Clean up data when needed
curl -X POST "http://localhost:8000/cleanup-data"
```

### **Generate Sample Data Directly**
```bash
# Run sample data generation script directly
python -c "from tasks.sample_data import generate_all_sample_data; generate_all_sample_data()"
```

### **What Sample Data Includes**

#### **Churches (5 churches)**
- First Baptist Church
- Grace Community Church  
- New Life Fellowship
- Trinity Methodist Church
- Hope Presbyterian Church

#### **Users (20 users)**
- 1 admin user
- 19 regular users (some may be blocked)
- Each user has a profile with nickname and optional church association

#### **Boards (8 discussion boards)**
- General Discussion
- Prayer Requests
- Bible Study
- Youth Ministry
- Worship & Music
- Community Service
- Family Life
- Testimonies

#### **Posts (50 posts)**
- Distributed across all boards
- Realistic titles and content
- Random view counts, like counts, and comment counts
- Various tags applied

#### **Comments (100 comments)**
- Distributed across posts
- Realistic comment content
- Proper author attribution

#### **Identity Verifications (10 verifications)**
- Some pending, some approved/rejected
- Linked to churches and users
- Admin review workflow

#### **Action Logs (200+ actions)**
- User interactions: views, likes, bookmarks, reports
- Distributed across posts and comments
- Realistic user behavior patterns

## 🔧 Test Configuration

### **Test Database**
Tests use a separate test database to avoid affecting your development data:
- Development DB: `fastapi_celery_db`
- Test DB: `test_fastapi_celery_db`

### **Test Fixtures**
- `client`: FastAPI test client
- `db_session`: Database session for direct DB operations
- `test_db`: Database setup/teardown

### **Environment Setup**
```bash
# Install test dependencies
poetry install

# Or manually install
pip install pytest pytest-asyncio httpx faker requests
```

## 📋 Test Categories

### **1. User Management Tests**
- User creation, retrieval, update, deletion
- Profile management
- UUID validation
- Error handling

### **2. Church Management Tests**
- Church CRUD operations
- Validation testing
- Pagination testing

### **3. Community Tests**
- Board management
- Post creation and management
- Comment system
- Post tagging
- View count tracking

### **4. Verification & Action Tests**
- Identity verification workflow
- Action logging (likes, bookmarks, etc.)
- Action toggling
- Count aggregation

### **5. Sample Data Tests**
- Data generation validation
- Foreign key integrity
- Data consistency
- Performance testing

## 🎯 Test Examples

### **Creating Test Data**
```python
def test_create_user(client):
    user_data = {
        "is_blocked": False,
        "is_admin": False
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert "id" in response.json()
```

### **Testing Relationships**
```python
def test_create_profile(client):
    # Create user first
    user_response = client.post("/users/", json={"is_blocked": False})
    user_id = user_response.json()["id"]
    
    # Create profile
    profile_data = {
        "user_id": user_id,
        "nickname": "testuser"
    }
    response = client.post("/users/profiles/", json=profile_data)
    assert response.status_code == 201
```

### **Testing Error Cases**
```python
def test_get_nonexistent_user(client):
    fake_id = str(uuid.uuid4())
    response = client.get(f"/users/{fake_id}")
    assert response.status_code == 404
```

## 🔍 Debugging Tests

### **Verbose Output**
```bash
pytest tests/ -v -s
```

### **Stop on First Failure**
```bash
pytest tests/ -x
```

### **Run Last Failed Tests**
```bash
pytest tests/ --lf
```

### **Coverage Report**
```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
```

## 📈 Performance Testing

### **Load Testing with Sample Data**
```bash
# Generate large dataset
python -c "
from tasks.sample_data import *
from database import SessionLocal
db = SessionLocal()
generate_sample_users(db, 100)
generate_sample_posts(db, boards, users, 500)
"

# Test API performance
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/users/"
```

### **Database Performance**
```python
# Test query performance
import time
start = time.time()
users = client.get("/users/?limit=100").json()
end = time.time()
print(f"Query took {end - start:.2f} seconds")
```

## 🛠️ Continuous Integration

### **GitHub Actions Example**
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      - name: Run tests
        run: poetry run pytest tests/ -v
```

## 🎨 Custom Test Data

### **Creating Custom Sample Data**
```python
# Create your own sample data function
def create_custom_test_data(db):
    # Create specific test scenario
    church = ChurchService.create_church(db, ChurchCreate(name="My Test Church"))
    user = UserService.create_user(db, UserCreate(is_admin=True))
    # ... more custom data
```

### **Test Data Factories**
```python
# Use factories for consistent test data
class UserFactory:
    @staticmethod
    def create_admin():
        return {"is_blocked": False, "is_admin": True}
    
    @staticmethod
    def create_regular():
        return {"is_blocked": False, "is_admin": False}
```

## 📚 Best Practices

### **Test Organization**
- Group related tests in classes
- Use descriptive test names
- Test both success and error cases
- Clean up test data properly

### **Sample Data Usage**
- Use sample data for development and demos
- Clean up sample data before production
- Generate realistic data for better testing
- Test with various data sizes

### **Performance Considerations**
- Use smaller datasets for unit tests
- Generate larger datasets for integration tests
- Monitor test execution time
- Use database transactions for test isolation

This comprehensive testing setup ensures your GoChurch Community Server is robust, reliable, and ready for production use!
