# Test Database Usage Guide

This guide explains how to use the test database system in GoChurch for API testing and unit testing.

## 🎯 **Overview**

The test database system provides:
- **Isolated testing environment** - Tests don't affect your main database
- **Automatic setup/cleanup** - Database is created and destroyed as needed
- **Sample data generation** - Realistic test data for comprehensive testing
- **Multiple testing approaches** - Unit tests, API tests, and manual testing

## 📊 **Database Configuration**

### **Main Database**
- URL: `postgresql://username:password@localhost:5432/fastapi_celery_db`
- Used for: Development and production

### **Test Database**
- URL: `postgresql://username:password@localhost:5432/test_fastapi_celery_db`
- Used for: All testing activities
- Automatically created/destroyed

## 🛠️ **Available Scripts**

### **1. Enhanced Test Runner**
```bash
# Run all tests with test database
python scripts/run_tests.py

# Run specific test file
python scripts/run_tests.py --pattern tests/test_users.py

# Run with verbose output
python scripts/run_tests.py --verbose

# Run with coverage report
python scripts/run_tests.py --coverage

# Run tests in parallel
python scripts/run_tests.py --parallel

# Database management options
python scripts/run_tests.py --create-db    # Create test database
python scripts/run_tests.py --drop-db      # Drop test database
python scripts/run_tests.py --reset-db     # Reset test database
```

### **2. API Testing with Test Database**
```bash
# Run comprehensive API tests
python scripts/test_api_with_testdb.py

# Setup test database only
python scripts/test_api_with_testdb.py --setup-only

# Cleanup test database only
python scripts/test_api_with_testdb.py --cleanup-only

# Skip automatic setup/cleanup
python scripts/test_api_with_testdb.py --no-setup --no-cleanup
```

### **3. Test Database Management**
```bash
# Create test database
python scripts/manage_test_db.py create

# Setup tables in test database
python scripts/manage_test_db.py setup

# Drop test database
python scripts/manage_test_db.py drop

# Reset test database (drop + create + setup)
python scripts/manage_test_db.py reset

# Show database information
python scripts/manage_test_db.py info
```

## 🧪 **Testing Workflows**

### **Unit Testing Workflow**
```bash
# 1. Run all unit tests (automatic test DB setup)
python scripts/run_tests.py

# 2. Run specific test suite
python scripts/run_tests.py --pattern tests/test_users.py --verbose

# 3. Run with coverage
python scripts/run_tests.py --coverage
```

### **API Testing Workflow**
```bash
# 1. Start your main server
./start.sh

# 2. Run API tests with isolated test data
python scripts/test_api_with_testdb.py

# 3. Check results and test database state
python scripts/manage_test_db.py info
```

### **Development Testing Workflow**
```bash
# 1. Setup test database with sample data
python scripts/test_api_with_testdb.py --setup-only

# 2. Run your tests/experiments
python scripts/run_tests.py --no-db-setup

# 3. Cleanup when done
python scripts/manage_test_db.py drop
```

## 🔧 **Configuration Options**

### **Environment Variables**
Add to your `.env` file:
```bash
# Optional: Explicit test database URL
TEST_DATABASE_URL=postgresql://username:password@localhost:5432/my_test_db

# Testing mode flag
TESTING=false
```

### **Test Configuration**
The test system automatically:
- Creates test database with `test_` prefix
- Enables UUID extension
- Creates all tables
- Generates sample data when needed
- Cleans up after tests

## 📋 **Test Database Features**

### **Automatic Setup**
- **UUID Extension**: Automatically enabled
- **Table Creation**: All models created automatically
- **Sample Data**: Generated on demand
- **Isolation**: Each test gets clean state

### **Sample Data Generation**
The test database can be populated with:
- **Users**: Test users with profiles
- **Churches**: Sample church directory
- **Boards**: Discussion boards
- **Posts**: Sample posts with engagement
- **Comments**: Nested comment threads
- **Verifications**: Identity verification requests
- **Actions**: User interaction logs

### **Transaction Management**
- **Unit Tests**: Each test runs in a transaction that's rolled back
- **API Tests**: Database is reset between test runs
- **Manual Tests**: You control when to setup/cleanup

## 🎯 **Best Practices**

### **For Unit Tests**
```python
def test_create_user(client, db_session, sample_user_data):
    """Test user creation with test database"""
    response = client.post("/users/", json=sample_user_data)
    assert response.status_code == 201
    # Transaction automatically rolled back after test
```

### **For API Tests**
```bash
# Always use the dedicated API testing script
python scripts/test_api_with_testdb.py

# Or setup test data manually
python scripts/test_api_with_testdb.py --setup-only
curl -X GET "http://localhost:8000/users/"
python scripts/manage_test_db.py drop
```

### **For Development**
```bash
# Create persistent test environment
python scripts/manage_test_db.py setup
python scripts/test_api_with_testdb.py --setup-only --no-cleanup

# Work with test data...
# Your API calls here

# Cleanup when done
python scripts/manage_test_db.py drop
```

## 🚨 **Troubleshooting**

### **Common Issues**

**Test database connection errors:**
```bash
# Check database configuration
python scripts/manage_test_db.py info

# Recreate test database
python scripts/manage_test_db.py reset
```

**Permission errors:**
```bash
# Make sure scripts are executable
chmod +x scripts/*.py

# Check database permissions
psql -h localhost -U username -d postgres -c "\l"
```

**Sample data generation fails:**
```bash
# Check dependencies
pip install faker sqlalchemy

# Reset and try again
python scripts/manage_test_db.py reset
python scripts/test_api_with_testdb.py --setup-only
```

### **Debugging Tips**

**Enable SQL logging:**
```python
# In tests/conftest.py, change:
test_engine = create_engine(TEST_DATABASE_URL, echo=True)
```

**Check test database state:**
```bash
# Connect to test database
psql -h localhost -U username -d test_fastapi_celery_db

# List tables
\dt

# Check data
SELECT COUNT(*) FROM users;
```

**Manual cleanup:**
```bash
# Force drop test database
python scripts/manage_test_db.py drop

# Or use SQL directly
psql -h localhost -U username -d postgres -c "DROP DATABASE IF EXISTS test_fastapi_celery_db"
```

## 📚 **Integration with Existing Tests**

Your existing test files automatically use the test database through the enhanced `conftest.py`. No changes needed to existing test code!

The test fixtures available:
- `client`: FastAPI test client
- `db_session`: Database session with rollback
- `clean_db_session`: Database session that commits
- `sample_user_data`: Sample user data
- `sample_church_data`: Sample church data
- `sample_board_data`: Sample board data

## 🎉 **Summary**

With this enhanced test database system, you can:

1. **Run isolated tests** without affecting your main database
2. **Generate realistic test data** for comprehensive testing
3. **Test APIs** with proper data setup and cleanup
4. **Debug issues** with dedicated test database tools
5. **Develop confidently** knowing tests won't break your data

The system handles all the complexity of database setup, sample data generation, and cleanup automatically!
