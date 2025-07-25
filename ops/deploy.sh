#!/bin/bash

# FastAPI Celery Application Deployment Script

set -e  # Exit on any error

echo "🚀 Starting FastAPI Celery Application Deployment"

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

echo "🧹 Cleaning up old images (optional)..."
docker-compose down --rmi local --volumes --remove-orphans 2>/dev/null || true

echo "🏗️  Building application image..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
echo "🔍 Checking service status..."
docker-compose ps

echo "📊 Checking logs..."
docker-compose logs --tail=20

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Application URLs:"
echo "   FastAPI: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   PostgreSQL: localhost:5432"
echo "   Redis: localhost:6379"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart: docker-compose restart"
echo "   Shell into app: docker-compose exec fastapi bash"
echo "   Database shell: docker-compose exec postgres psql -U fastapi_user -d fastapi_celery_db"
