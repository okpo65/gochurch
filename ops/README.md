# FastAPI Celery Application - Docker Deployment

This directory contains Docker Compose configurations for easy deployment of the FastAPI Celery application on any server.

## Quick Start

### Production Deployment

1. **Copy the ops folder to your server**
2. **Set up environment variables**:
   ```bash
   cd ops
   cp .env.docker .env
   # Edit .env with your configuration
   ```
3. **Deploy**:
   ```bash
   ./deploy.sh
   ```

### Development Mode

For local development with hot reload:
```bash
./dev.sh
```

## Files Overview

### Docker Compose Files
- `docker-compose.yml` - Production configuration
- `docker-compose.dev.yml` - Development configuration with hot reload

### Dockerfiles
- `Dockerfile` - Production image (optimized, no dev dependencies)
- `Dockerfile.dev` - Development image (includes dev dependencies, hot reload)

### Scripts
- `deploy.sh` - Production deployment script
- `dev.sh` - Development deployment script
- `init-db.sql` - Database initialization script

### Configuration
- `.env.docker` - Environment variables template
- `.env` - Your actual environment variables (create from template)

## Services

The application consists of 4 services:

1. **postgres** - PostgreSQL 14 database
2. **redis** - Redis for Celery message broker
3. **fastapi** - FastAPI web application
4. **celery** - Celery worker for background tasks

## Environment Variables

Key variables to configure in `.env`:

```bash
# Database
POSTGRES_DB=fastapi_celery_db
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=your_secure_password

# Application
SECRET_KEY=your-production-secret-key
DEBUG=False
ENVIRONMENT=production

# Ports
POSTGRES_PORT=5432
REDIS_PORT=6379
FASTAPI_PORT=8000
```

## Deployment Commands

### Production
```bash
# Deploy
./deploy.sh

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart specific service
docker-compose restart fastapi

# Shell into application
docker-compose exec fastapi bash

# Database shell
docker-compose exec postgres psql -U fastapi_user -d fastapi_celery_db

# Run database migrations
docker-compose exec fastapi alembic upgrade head
```

### Development
```bash
# Start development environment
./dev.sh

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop
docker-compose -f docker-compose.dev.yml down
```

## Server Requirements

### Minimum Requirements
- Docker 20.10+
- Docker Compose 2.0+
- 1GB RAM
- 10GB disk space

### Recommended
- 2GB+ RAM
- 20GB+ disk space
- SSD storage

## Port Configuration

Default ports:
- **8000** - FastAPI application
- **5432** - PostgreSQL database
- **6379** - Redis

To change ports, edit the `ports` section in docker-compose.yml:
```yaml
services:
  fastapi:
    ports:
      - "8080:8000"  # Change external port to 8080
```

## Data Persistence

Data is persisted in Docker volumes:
- `postgres_data` - Database data
- `redis_data` - Redis data

To backup data:
```bash
# Backup database
docker-compose exec postgres pg_dump -U fastapi_user fastapi_celery_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U fastapi_user fastapi_celery_db < backup.sql
```

## SSL/HTTPS Setup

For production, add a reverse proxy (nginx) or use a service like Cloudflare.

Example nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring

### Health Checks
Services include health checks. Check status:
```bash
docker-compose ps
```

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fastapi
docker-compose logs -f celery
```

### Resource Usage
```bash
docker stats
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   # Kill the process or change port in docker-compose.yml
   ```

2. **Database connection failed**
   ```bash
   # Check if postgres is healthy
   docker-compose ps
   # View postgres logs
   docker-compose logs postgres
   ```

3. **Celery worker not starting**
   ```bash
   # Check redis connection
   docker-compose logs redis
   # Check celery logs
   docker-compose logs celery
   ```

### Reset Everything
```bash
# Stop and remove everything
docker-compose down --volumes --rmi all

# Start fresh
./deploy.sh
```

## Security Considerations

1. **Change default passwords** in `.env`
2. **Use strong SECRET_KEY**
3. **Don't expose database ports** in production
4. **Use HTTPS** with reverse proxy
5. **Regular updates** of Docker images
6. **Backup data** regularly

## Scaling

To scale Celery workers:
```bash
docker-compose up -d --scale celery=3
```

For high availability, consider:
- Multiple application instances behind load balancer
- External PostgreSQL service (AWS RDS, etc.)
- External Redis service (AWS ElastiCache, etc.)
- Container orchestration (Kubernetes, Docker Swarm)
