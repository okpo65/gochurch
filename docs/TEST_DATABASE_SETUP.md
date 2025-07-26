# Test Database Setup Guide

This guide explains how to set up a separate test database with its own port for complete isolation from your main database.

## 🎯 **Why Separate Ports?**

Using separate ports for test and main databases provides:
- **Complete Isolation**: Test data never interferes with production data
- **Parallel Operations**: Run tests while main application is running
- **Safety**: Impossible to accidentally affect main database during testing
- **Performance**: Dedicated resources for testing

## 🏗️ **Database Architecture**

```
Main Database (Production/Development)
├── Host: localhost
├── Port: 5432
├── Database: fastapi_celery_db
└── Usage: Main application

Test Database (Testing Only)
├── Host: localhost  
├── Port: 5433
├── Database: test_fastapi_celery_db
└── Usage: Unit tests, API tests, development testing
```

## 🔧 **Setup Options**

### **Option 1: Separate PostgreSQL Instance (Recommended)**

Run a dedicated PostgreSQL instance for testing:

```bash
# 1. Create test data directory
mkdir -p ~/postgres_test_data

# 2. Initialize test database cluster
initdb -D ~/postgres_test_data

# 3. Start test PostgreSQL on port 5433
pg_ctl -D ~/postgres_test_data -o "-p 5433" start

# 4. Create test user and database
createuser -h localhost -p 5433 username
createdb -h localhost -p 5433 -O username test_fastapi_celery_db

# 5. Test connection
psql -h localhost -p 5433 -U username -d test_fastapi_celery_db -c "SELECT version();"
```

### **Option 2: Same Instance, Different Port (Alternative)**

If you prefer using the same PostgreSQL instance:

```bash
# Update your .env file to use the same port for testing
TEST_DB_PORT=5432
```

### **Option 3: Docker Setup**

Use Docker for test database:

```bash
# Start test PostgreSQL container
docker run -d \
  --name postgres-test \
  -e POSTGRES_USER=username \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=test_fastapi_celery_db \
  -p 5433:5432 \
  postgres:13

# Test connection
psql -h localhost -p 5433 -U username -d test_fastapi_celery_db -c "SELECT version();"
```

## ⚙️ **Configuration**

### **Environment Variables**

Update your `.env` file:

```bash
# Main Database
DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_celery_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_celery_db
DB_USER=username
DB_PASSWORD=password

# Test Database (Separate Port)
TEST_DB_HOST=localhost
TEST_DB_PORT=5433
TEST_DB_NAME=test_fastapi_celery_db
TEST_DB_USER=username
TEST_DB_PASSWORD=password

# Optional: Explicit test database URL
# TEST_DATABASE_URL=postgresql://username:password@localhost:5433/test_fastapi_celery_db
```

### **Automatic Configuration**

The system automatically generates the test database URL:
- **Method**: Uses `settings.get_test_database_url()`
- **Default**: `postgresql://username:password@localhost:5433/test_fastapi_celery_db`
- **Override**: Set `TEST_DATABASE_URL` environment variable

## 🧪 **Testing the Setup**

### **1. Check Database Connectivity**

```bash
# Check both databases
python scripts/manage_test_db.py check

# Expected output:
# ✅ Main database accessible: postgresql://...
# ✅ Test database server accessible on port 5433
```

### **2. Create Test Database**

```bash
# Create and setup test database
python scripts/manage_test_db.py setup

# Expected output:
# ✅ Created test database: test_fastapi_celery_db on port 5433
# ✅ Test database tables created on port 5433
```

### **3. Run Tests**

```bash
# Run unit tests
python scripts/run_tests.py

# Run API tests
python scripts/test_api_with_testdb.py
```

## 🛠️ **Available Commands**

### **Database Management**

```bash
# Check connectivity
python scripts/manage_test_db.py check

# Create test database
python scripts/manage_test_db.py create

# Setup tables
python scripts/manage_test_db.py setup

# Drop test database
python scripts/manage_test_db.py drop

# Reset (drop + create + setup)
python scripts/manage_test_db.py reset

# Show configuration
python scripts/manage_test_db.py info
```

### **Test Execution**

```bash
# Unit tests with automatic DB setup
python scripts/run_tests.py

# Unit tests with verbose output
python scripts/run_tests.py --verbose

# API tests with test data
python scripts/test_api_with_testdb.py

# Check database connectivity only
python scripts/run_tests.py --check-db
```

## 🚨 **Troubleshooting**

### **Connection Refused Errors**

```bash
# Error: connection to server at "localhost" (127.0.0.1), port 5433 failed
```

**Solutions:**
1. **Start test PostgreSQL instance:**
   ```bash
   pg_ctl -D ~/postgres_test_data -o "-p 5433" start
   ```

2. **Check if port is in use:**
   ```bash
   lsof -i :5433
   ```

3. **Use same port as main database:**
   ```bash
   # In .env file
   TEST_DB_PORT=5432
   ```

### **Database Does Not Exist**

```bash
# Error: database "test_fastapi_celery_db" does not exist
```

**Solution:**
```bash
# Create the database
python scripts/manage_test_db.py create
```

### **Permission Denied**

```bash
# Error: permission denied for database
```

**Solution:**
```bash
# Create user with proper permissions
createuser -h localhost -p 5433 -s username
```

### **UUID Extension Error**

```bash
# Error: extension "uuid-ossp" does not exist
```

**Solution:**
```bash
# Connect as superuser and create extension
psql -h localhost -p 5433 -U postgres -d test_fastapi_celery_db -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
```

## 🎯 **Best Practices**

### **Development Workflow**

1. **Start test database:**
   ```bash
   pg_ctl -D ~/postgres_test_data -o "-p 5433" start
   ```

2. **Run tests:**
   ```bash
   python scripts/run_tests.py
   ```

3. **Stop test database when done:**
   ```bash
   pg_ctl -D ~/postgres_test_data stop
   ```

### **Continuous Integration**

For CI/CD pipelines:

```yaml
# Example GitHub Actions
services:
  postgres-test:
    image: postgres:13
    env:
      POSTGRES_USER: username
      POSTGRES_PASSWORD: password
      POSTGRES_DB: test_fastapi_celery_db
    ports:
      - 5433:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

### **Local Development**

```bash
# Add to your shell profile (.bashrc, .zshrc)
alias start-test-db="pg_ctl -D ~/postgres_test_data -o '-p 5433' start"
alias stop-test-db="pg_ctl -D ~/postgres_test_data stop"
alias test-gochurch="python scripts/run_tests.py"
```

## 📊 **Monitoring**

### **Check Database Status**

```bash
# Check if test database is running
pg_ctl -D ~/postgres_test_data status

# Check connections
psql -h localhost -p 5433 -U username -d test_fastapi_celery_db -c "SELECT count(*) FROM pg_stat_activity;"
```

### **Database Size**

```bash
# Check test database size
psql -h localhost -p 5433 -U username -d test_fastapi_celery_db -c "SELECT pg_size_pretty(pg_database_size('test_fastapi_celery_db'));"
```

## 🎉 **Summary**

With this setup, you have:

1. **Complete Isolation**: Test database on separate port (5433)
2. **Automatic Management**: Scripts handle database creation/cleanup
3. **Flexible Testing**: Unit tests, API tests, and manual testing
4. **Safety**: No risk of affecting main database
5. **Performance**: Dedicated resources for testing

The system automatically handles all the complexity while providing you with powerful testing capabilities!
