# Docker Troubleshooting Guide

## 🔧 Common Docker Issues & Solutions

### **Poetry Installation Failed**

**Error**: `process "/bin/sh -c poetry config virtualenvs.create false && poetry install" did not complete successfully`

**Solutions**:

#### **1. Clear Docker Cache**
```bash
# Remove all Docker images and rebuild
docker system prune -a
cd ops
docker-compose build --no-cache
```

#### **2. Check Poetry Version**
The Dockerfile now uses a specific Poetry version (1.6.1) to avoid compatibility issues.

#### **3. Check pyproject.toml**
Ensure your `pyproject.toml` is valid:
```bash
# Validate locally first
poetry check
poetry install --dry-run
```

#### **4. Build Step by Step**
```bash
# Build only the FastAPI service to isolate issues
docker-compose build fastapi

# Check build logs
docker-compose build fastapi --progress=plain
```

### **Import Errors in Container**

**Error**: `ModuleNotFoundError: No module named 'config'`

**Solution**: The project structure has been updated. Make sure you're using the latest Docker files that include the correct import paths.

### **Database Connection Issues**

**Error**: `could not connect to server: Connection refused`

**Solutions**:

#### **1. Check Service Dependencies**
```bash
# Ensure services start in correct order
docker-compose up postgres redis
# Wait for them to be healthy, then:
docker-compose up fastapi celery
```

#### **2. Check Health Checks**
```bash
# View service status
docker-compose ps

# Check logs
docker-compose logs postgres
docker-compose logs redis
```

#### **3. Manual Database Connection Test**
```bash
# Connect to database manually
docker-compose exec postgres psql -U fastapi_user -d fastapi_celery_db
```

### **Alembic Migration Issues**

**Error**: `alembic.util.exc.CommandError: Can't locate revision identified by`

**Solutions**:

#### **1. Reset Migrations**
```bash
# Connect to container
docker-compose exec fastapi bash

# Reset alembic
rm -rf config/alembic/versions/*
alembic -c config/alembic.ini revision --autogenerate -m "Initial migration"
alembic -c config/alembic.ini upgrade head
```

#### **2. Manual Migration**
```bash
# Skip migrations and create tables directly
docker-compose exec fastapi python -c "from database import create_tables; create_tables()"
```

### **Port Already in Use**

**Error**: `port is already allocated`

**Solutions**:

#### **1. Stop Conflicting Services**
```bash
# Stop local services
brew services stop postgresql
brew services stop redis

# Or change ports in docker-compose.yml
```

#### **2. Find and Kill Process**
```bash
# Find what's using port 8000
lsof -i :8000
kill -9 <PID>
```

### **Volume Mount Issues**

**Error**: Permission denied or file not found in mounted volumes

**Solutions**:

#### **1. Fix Permissions**
```bash
# Fix ownership
sudo chown -R $USER:$USER .

# Or run container as root temporarily
docker-compose exec --user root fastapi bash
```

#### **2. Check Volume Mounts**
```bash
# Verify mounts are correct
docker-compose config
```

## 🚀 **Quick Fixes**

### **Complete Reset**
```bash
# Nuclear option - reset everything
docker-compose down --volumes --remove-orphans
docker system prune -a
docker volume prune
cd ops
./deploy.sh
```

### **Development vs Production**
```bash
# For development (with hot reload)
cd ops
docker-compose -f docker-compose.dev.yml up --build

# For production
cd ops
docker-compose up --build
```

### **Check Container Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fastapi
docker-compose logs -f postgres
docker-compose logs -f celery
```

### **Shell Access**
```bash
# Access FastAPI container
docker-compose exec fastapi bash

# Access PostgreSQL
docker-compose exec postgres psql -U fastapi_user -d fastapi_celery_db

# Access Redis
docker-compose exec redis redis-cli
```

## 🔍 **Debugging Steps**

### **1. Verify Docker Setup**
```bash
docker --version
docker-compose --version
docker info
```

### **2. Check Service Health**
```bash
docker-compose ps
docker-compose top
```

### **3. Test Individual Components**
```bash
# Test database
docker-compose exec postgres pg_isready -U fastapi_user

# Test Redis
docker-compose exec redis redis-cli ping

# Test API
curl http://localhost:8000/
```

### **4. Monitor Resources**
```bash
# Check resource usage
docker stats

# Check disk space
docker system df
```

## 📋 **Environment Variables**

Make sure your `.env` file in the `ops/` directory contains:

```env
# Database
POSTGRES_DB=fastapi_celery_db
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=your_secure_password

# Application
SECRET_KEY=your-secret-key-here
DEBUG=False
ENVIRONMENT=production

# Redis
REDIS_URL=redis://redis:6379/0
```

## 🆘 **Getting Help**

If you're still having issues:

1. **Check the main troubleshooting guide**: `docs/TROUBLESHOOTING.md`
2. **Review Docker logs**: `docker-compose logs -f`
3. **Test locally first**: Make sure the app works without Docker
4. **Check Docker resources**: Ensure you have enough RAM/disk space
5. **Try development mode**: Use `docker-compose.dev.yml` for easier debugging

## 🎯 **Success Indicators**

You know Docker is working when:
- ✅ `docker-compose ps` shows all services as "Up"
- ✅ `curl http://localhost:8000/` returns JSON response
- ✅ `curl http://localhost:8000/docs` loads Swagger UI
- ✅ No error messages in `docker-compose logs`
