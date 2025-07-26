# 🧪 Test Environment Quick Setup Guide

## 🚀 **One-Command Setup**

```bash
# Complete setup (database + tests)
./setup_tests.sh

# Setup only (no tests)
./setup_tests.sh --setup-only
```

## 🔧 **Manual Setup Steps**

### **1. Environment Configuration**
Your `.env` file is already configured with:
- **Main Database**: `postgresql://jihwan@localhost:5432/fastapi_celery_db`
- **Test Database**: `postgresql://jihwan@localhost:5433/test_fastapi_celery_db`

### **2. Test Database Hosting**

```bash
# Setup test database host (one-time)
poetry run python scripts/setup_test_db_host.py setup

# Or individual steps:
poetry run python scripts/setup_test_db_host.py init    # Initialize
poetry run python scripts/setup_test_db_host.py start   # Start
poetry run python scripts/setup_test_db_host.py status  # Check status
```

### **3. Run Tests**

```bash
# Run all tests
poetry run python scripts/run_tests.py

# Run specific test file
poetry run python scripts/run_tests.py --pattern tests/test_users.py

# Run API tests
poetry run python scripts/test_api_with_testdb.py
```

## 🗄️ **Database Management**

### **Test Database Host Control**
```bash
# Start test database
poetry run python scripts/setup_test_db_host.py start

# Stop test database
poetry run python scripts/setup_test_db_host.py stop

# Check status
poetry run python scripts/setup_test_db_host.py status

# Restart
poetry run python scripts/setup_test_db_host.py restart

# Complete cleanup
poetry run python scripts/setup_test_db_host.py cleanup
```

### **Test Database Management**
```bash
# Check connectivity
poetry run python scripts/manage_test_db.py check

# Create test database
poetry run python scripts/manage_test_db.py create

# Setup tables
poetry run python scripts/manage_test_db.py setup

# Show configuration
poetry run python scripts/manage_test_db.py info
```

## 📊 **Current Configuration**

Based on your `.env` file:

| Component | Main | Test |
|-----------|------|------|
| **Host** | localhost | localhost |
| **Port** | 5432 | 5433 |
| **Database** | fastapi_celery_db | test_fastapi_celery_db |
| **User** | jihwan | jihwan |
| **Redis DB** | 0 | 1 |

## 🎯 **Quick Commands**

```bash
# Complete setup
./setup_tests.sh

# Just setup database hosting
poetry run python scripts/setup_test_db_host.py setup

# Run tests only
poetry run python scripts/run_tests.py

# Check everything is working
poetry run python scripts/manage_test_db.py check
```

## 🚨 **Troubleshooting**

### **PostgreSQL Not Found**
```bash
# Install PostgreSQL
brew install postgresql

# Or check if it's in PATH
which psql
```

### **Port 5433 Already in Use**
```bash
# Check what's using the port
lsof -i :5433

# Or use a different port in .env
TEST_DB_PORT=5434
```

### **Permission Denied**
```bash
# Make sure user exists
createuser -s jihwan

# Or run as postgres user
sudo -u postgres createuser -s jihwan
```

### **Test Database Connection Failed**
```bash
# Check if test database is running
poetry run python scripts/setup_test_db_host.py status

# Restart test database
poetry run python scripts/setup_test_db_host.py restart
```

## 🎉 **Success Indicators**

When everything is working, you should see:
- ✅ Test database running on port 5433
- ✅ All unit tests passing
- ✅ API tests connecting to test database
- ✅ No interference with main database

## 📋 **Daily Workflow**

```bash
# Start your day
./setup_tests.sh --setup-only

# During development
poetry run python scripts/run_tests.py

# When done
poetry run python scripts/setup_test_db_host.py stop
```
