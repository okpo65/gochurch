#!/bin/bash

# GoChurch Community Server Deployment Script

set -e  # Exit on any error

echo "🚀 Starting GoChurch Community Server Deployment (Production)"
echo "=" * 60

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Navigate to ops directory
cd "$(dirname "$0")"

# Check if .env file exists, if not copy from template
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.docker .env
    echo "⚠️  Please edit ops/.env file with your configuration before running again."
    echo "   Especially change the SECRET_KEY and database passwords!"
    exit 1
fi

echo "🛑 Stopping existing containers..."
docker-compose down

echo "🧹 Cleaning up old images..."
docker-compose down --rmi local --volumes --remove-orphans 2>/dev/null || true

echo "🏗️  Building application images..."
docker-compose build --no-cache

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to be healthy..."
sleep 15

# Check service health
echo "🔍 Checking service status..."
docker-compose ps

# Check if FastAPI is responding
echo "🌐 Testing API endpoint..."
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ API is responding!"
else
    echo "⚠️  API might still be starting up..."
fi

echo "📊 Recent logs:"
docker-compose logs --tail=10

echo ""
echo "🎉 Deployment complete!"
echo "=" * 60
echo ""
echo "🌐 Application URLs:"
echo "   - FastAPI: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo ""
echo "📋 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart: docker-compose restart"
echo "   - Shell into app: docker-compose exec fastapi bash"
echo "   - Database shell: docker-compose exec postgres psql -U fastapi_user -d fastapi_celery_db"
echo "   - Generate sample data: curl -X POST http://localhost:8000/generate-sample-data"
echo ""
echo "🔧 Troubleshooting:"
echo "   - If services fail to start, check: docker-compose logs"
echo "   - For database issues, check: docker-compose logs postgres"
echo "   - For app issues, check: docker-compose logs fastapi"
