# 🐳 Docker Deployment Guide

This guide explains how to use Docker for GoChurch development and production deployment with environment variables and test database hosting.

## 🏗️ **Architecture**

### **Services**
- **postgres**: Main PostgreSQL database (port 5432)
- **postgres_test**: Test PostgreSQL database (port 5433)
- **redis**: Redis for caching and Celery (port 6379)
- **fastapi**: Main FastAPI application (port 8000)
- **celery**: Celery worker for background tasks
- **test_runner**: Automated test execution service

### **Profiles**
- **default**: Main application services only
- **test**: Includes test database
- **full**: All services including test runner

## 🔧 **Environment Configuration**

### **Environment Files**
- **`.env`**: Main environment variables (used by default)
- **`ops/.env.docker`**: Docker-specific overrides
- **`.env.production`**: Production environment variables

### **Key Variables from Your .env**
```bash
# Database Configuration
DB_NAME=fastapi_celery_db
DB_USER=jihwan
DB_PASSWORD=
DB_PORT=5432

# Test Database Configuration
TEST_DB_NAME=test_fastapi_celery_db
TEST_DB_USER=jihwan
TEST_DB_PASSWORD=
TEST_DB_PORT=5433

# Redis Configuration
REDIS_PORT=6379
REDIS_DB=0
TEST_REDIS_DB=1
```

## 🚀 **Development Usage**

### **Quick Start**
```bash
# Start main services
cd ops
./docker-dev.sh up

# Start with test database
./docker-dev.sh up-test

# Start everything including test runner
./docker-dev.sh up-full
```

### **Available Commands**
```bash
./docker-dev.sh up          # Start main services
./docker-dev.sh up-test     # Start with test database
./docker-dev.sh up-full     # Start all services
./docker-dev.sh down        # Stop all services
./docker-dev.sh restart     # Restart services
./docker-dev.sh logs        # Show all logs
./docker-dev.sh logs-app    # Show FastAPI logs only
./docker-dev.sh test        # Run tests in Docker
./docker-dev.sh build       # Build all images
./docker-dev.sh clean       # Clean up everything
./docker-dev.sh status      # Show service status
```

## 🧪 **Testing in Docker**

### **Run Tests**
```bash
# Run tests with test database
cd ops
./docker-dev.sh test

# Or manually
docker-compose --env-file ../.env --profile test up test_runner
```

### **Test Database Access**
```bash
# Connect to test database
docker-compose exec postgres_test psql -U jihwan -d test_fastapi_celery_db

# Check test database status
docker-compose ps postgres_test
```

## 🏭 **Production Deployment**

### **Setup Production Environment**
```bash
# Create production environment file
cp .env .env.production

# Edit production settings
nano .env.production
```

**Required Production Changes:**
```bash
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-strong-production-secret-key
DB_PASSWORD=strong-production-password
```

### **Deploy to Production**
```bash
cd ops
./docker-prod.sh deploy     # Initial deployment
./docker-prod.sh update     # Update existing deployment
./docker-prod.sh backup     # Backup database
./docker-prod.sh status     # Check status
```

## 📊 **Service Details**

### **Main PostgreSQL (postgres)**
- **Image**: postgres:14-alpine
- **Port**: 5432 (mapped from .env DB_PORT)
- **Database**: fastapi_celery_db (from .env DB_NAME)
- **User**: jihwan (from .env DB_USER)
- **Volume**: postgres_data
- **Health Check**: pg_isready

### **Test PostgreSQL (postgres_test)**
- **Image**: postgres:14-alpine
- **Port**: 5433 (mapped from .env TEST_DB_PORT)
- **Database**: test_fastapi_celery_db (from .env TEST_DB_NAME)
- **User**: jihwan (from .env TEST_DB_USER)
- **Volume**: postgres_test_data
- **Profile**: test, full

### **Redis**
- **Image**: redis:7-alpine
- **Port**: 6379 (mapped from .env REDIS_PORT)
- **Volume**: redis_data
- **Persistence**: Enabled with appendonly

### **FastAPI Application**
- **Build**: Custom Dockerfile
- **Port**: 8000
- **Environment**: All .env variables passed through
- **Volumes**: .env file, alembic configs
- **Command**: uvicorn with reload in development

### **Test Runner**
- **Build**: Custom Dockerfile.test
- **Environment**: Test-specific variables
- **Volumes**: Tests, scripts, .env
- **Profile**: test, full
- **Command**: python scripts/run_tests.py --verbose

## 🔍 **Monitoring and Debugging**

### **View Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fastapi
docker-compose logs -f postgres_test

# Last 100 lines
docker-compose logs --tail=100 fastapi
```

### **Execute Commands in Containers**
```bash
# Connect to FastAPI container
docker-compose exec fastapi bash

# Run database migrations
docker-compose exec fastapi poetry run alembic upgrade head

# Connect to main database
docker-compose exec postgres psql -U jihwan -d fastapi_celery_db

# Connect to test database
docker-compose exec postgres_test psql -U jihwan -d test_fastapi_celery_db
```

### **Check Service Health**
```bash
# Service status
docker-compose ps

# Resource usage
docker stats

# Network information
docker network ls
docker network inspect ops_gochurch_network
```

## 🗄️ **Database Management**

### **Backup and Restore**
```bash
# Backup main database
docker-compose exec postgres pg_dump -U jihwan fastapi_celery_db > backup.sql

# Restore main database
docker-compose exec -T postgres psql -U jihwan fastapi_celery_db < backup.sql

# Backup test database
docker-compose exec postgres_test pg_dump -U jihwan test_fastapi_celery_db > test_backup.sql
```

### **Database Migrations**
```bash
# Run migrations on main database
docker-compose exec fastapi poetry run alembic upgrade head

# Create new migration
docker-compose exec fastapi poetry run alembic revision --autogenerate -m "Description"
```

## 🔧 **Troubleshooting**

### **Common Issues**

**Port Already in Use:**
```bash
# Check what's using the port
lsof -i :5432
lsof -i :5433

# Change ports in .env file
DB_PORT=5434
TEST_DB_PORT=5435
```

**Database Connection Failed:**
```bash
# Check if database is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

**Test Database Not Accessible:**
```bash
# Make sure test profile is active
docker-compose --profile test up -d

# Check test database status
docker-compose ps postgres_test

# Restart test database
docker-compose restart postgres_test
```

**Environment Variables Not Loading:**
```bash
# Check .env file exists
ls -la ../.env

# Verify environment variables in container
docker-compose exec fastapi env | grep DB_
```

### **Reset Everything**
```bash
# Stop and remove everything
cd ops
./docker-dev.sh clean

# Start fresh
./docker-dev.sh up-test
```

## 📋 **Best Practices**

### **Development**
- Use `up-test` profile for development with testing
- Keep .env file updated with your local settings
- Use `logs-app` for focused debugging
- Run tests regularly with `./docker-dev.sh test`

### **Production**
- Always use `.env.production` for production
- Set strong passwords and secret keys
- Regular database backups with `./docker-prod.sh backup`
- Monitor logs and resource usage
- Use health checks for service monitoring

### **Testing**
- Test database runs on separate port (5433)
- Tests use separate Redis database (DB 1)
- Test data is isolated from main application
- Use test_runner service for automated testing

## 🎯 **Quick Reference**

```bash
# Development
cd ops
./docker-dev.sh up-test        # Start with test DB
./docker-dev.sh test           # Run tests
./docker-dev.sh logs-app       # Check app logs

# Production
./docker-prod.sh deploy        # Deploy
./docker-prod.sh backup        # Backup
./docker-prod.sh status        # Monitor

# Database
docker-compose exec postgres psql -U jihwan -d fastapi_celery_db
docker-compose exec postgres_test psql -U jihwan -d test_fastapi_celery_db

# Cleanup
./docker-dev.sh clean          # Remove everything
```

Your Docker environment now fully supports your .env configuration with separate test database hosting!
