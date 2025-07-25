# GoChurch Community Server - Troubleshooting Guide

## 🔧 Common Issues and Solutions

### 1. UUID Extension Error

**Error**: `sqlalchemy.exc.ObjectNotExecutableError: Not an executable object: 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'`

**Solutions**:

#### Option A: Use the Fixed Version (Recommended)
The error has been fixed in the updated `database.py`. The UUID extension is now created using proper SQLAlchemy syntax:

```python
with engine.begin() as conn:
    conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
```

#### Option B: Use Python UUID Generation
If you don't have PostgreSQL extension privileges, use Python's UUID generation:

```bash
python setup_uuid_alternative.py
```

This approach:
- Uses Python's `uuid.uuid4()` instead of PostgreSQL's `uuid_generate_v4()`
- Doesn't require database extensions
- Works with any database that supports UUID type

#### Option C: Manual Extension Creation
If you have database admin access, manually create the extension:

```sql
-- Connect to your database as superuser
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### 2. Database Connection Issues

**Error**: Database connection failed

**Solutions**:

1. **Check PostgreSQL is running**:
   ```bash
   # macOS with Homebrew
   brew services list | grep postgresql
   brew services start postgresql
   
   # Linux
   sudo systemctl status postgresql
   sudo systemctl start postgresql
   ```

2. **Verify database exists**:
   ```bash
   psql -h localhost -U your_username -l
   ```

3. **Check .env configuration**:
   ```bash
   # Verify your .env file has correct values
   cat .env | grep DATABASE
   ```

4. **Test connection manually**:
   ```bash
   psql "postgresql://username:password@localhost:5432/database_name"
   ```

### 3. Migration Issues

**Error**: Migration script fails

**Solutions**:

1. **Run the enhanced migration script**:
   ```bash
   python migrate_to_uuid_schema.py
   ```

2. **Check database permissions**:
   ```sql
   -- Your user needs these permissions
   GRANT CREATE ON DATABASE your_database TO your_user;
   GRANT USAGE ON SCHEMA public TO your_user;
   GRANT CREATE ON SCHEMA public TO your_user;
   ```

3. **Manual table creation**:
   ```bash
   # If migration fails, try creating tables manually
   python -c "from database import create_tables; create_tables()"
   ```

### 4. Import Errors

**Error**: Module import errors

**Solutions**:

1. **Install dependencies**:
   ```bash
   poetry install
   # or
   pip install -r requirements.txt
   ```

2. **Check Python path**:
   ```bash
   # Make sure you're in the project directory
   pwd
   # Should show: /path/to/gochurch
   ```

3. **Activate virtual environment**:
   ```bash
   poetry shell
   # or
   source venv/bin/activate
   ```

### 5. Server Startup Issues

**Error**: Server won't start

**Solutions**:

1. **Check port availability**:
   ```bash
   lsof -i :8000
   # Kill process if port is in use
   kill -9 <PID>
   ```

2. **Start with verbose logging**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
   ```

3. **Check Celery worker**:
   ```bash
   celery -A celery_app worker --loglevel=info
   ```

### 6. Swagger Documentation Issues

**Error**: Documentation not loading

**Solutions**:

1. **Clear browser cache** and reload `/docs`

2. **Check FastAPI version**:
   ```bash
   pip show fastapi
   # Should be 0.104.1 or higher
   ```

3. **Verify OpenAPI schema**:
   ```bash
   curl http://localhost:8000/openapi.json
   ```

## 🚀 Setup Verification

### Quick Health Check
```bash
# 1. Test database connection
python -c "from database import engine; print('DB OK' if engine.connect() else 'DB FAIL')"

# 2. Test table creation
python -c "from database import create_tables; create_tables(); print('Tables OK')"

# 3. Test server startup
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
sleep 5
curl http://localhost:8000/
```

### Complete Setup Verification
```bash
# Run the migration script
python migrate_to_uuid_schema.py

# Start the server
./start.sh

# Test API endpoints
curl -X POST "http://localhost:8000/churches/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Church", "address": "123 Test St"}'

# Check documentation
open http://localhost:8000/docs
```

## 🔍 Debugging Tips

### 1. Enable Debug Mode
```python
# In main.py
app = FastAPI(debug=True)
```

### 2. Check Logs
```bash
# Server logs
tail -f logs/server.log

# Database logs (if enabled)
tail -f logs/database.log
```

### 3. SQL Query Debugging
```python
# Add to database.py for SQL logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### 4. Test Individual Components
```python
# Test database models
python -c "from app.user.models import User; print('Models OK')"

# Test services
python -c "from app.user.service import UserService; print('Services OK')"

# Test schemas
python -c "from app.user.schemas import UserCreate; print('Schemas OK')"
```

## 📞 Getting Help

### 1. Check Error Messages
- Read the full error traceback
- Look for the root cause (usually at the bottom)
- Check line numbers and file names

### 2. Common Error Patterns
- **Import errors**: Usually missing dependencies or wrong Python path
- **Database errors**: Connection issues or permission problems
- **UUID errors**: Extension or type support issues
- **Server errors**: Port conflicts or configuration problems

### 3. Environment Information
When reporting issues, include:
```bash
# System info
python --version
pip list | grep -E "(fastapi|sqlalchemy|psycopg2)"
psql --version

# Database info
echo $DATABASE_URL
```

### 4. Reset Everything
If all else fails, start fresh:
```bash
# Drop and recreate database
dropdb your_database_name
createdb your_database_name

# Reinstall dependencies
rm -rf .venv
poetry install

# Run migration
python migrate_to_uuid_schema.py
```

## ✅ Success Indicators

You know everything is working when:
- ✅ Migration script completes without errors
- ✅ Server starts on http://localhost:8000
- ✅ Swagger docs load at http://localhost:8000/docs
- ✅ API endpoints return proper JSON responses
- ✅ Database queries execute successfully
- ✅ UUID generation works properly

If you're still having issues after trying these solutions, check the specific error message and look for similar patterns in this guide.
