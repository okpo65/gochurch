#!/bin/bash

# Development deployment script with hot reload

set -e

echo "🚀 Starting FastAPI Celery Application (Development Mode)"

cd "$(dirname "$0")"

echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.dev.yml down

echo "🏗️  Building development image..."
docker-compose -f docker-compose.dev.yml build

echo "🚀 Starting development services..."
docker-compose -f docker-compose.dev.yml up -d

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔍 Checking service status..."
docker-compose -f docker-compose.dev.yml ps

echo ""
echo "✅ Development environment ready!"
echo ""
echo "🌐 Application URLs:"
echo "   FastAPI: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Development commands:"
echo "   View logs: docker-compose -f docker-compose.dev.yml logs -f"
echo "   Stop: docker-compose -f docker-compose.dev.yml down"
echo "   Shell: docker-compose -f docker-compose.dev.yml exec fastapi bash"
echo ""
echo "🔥 Hot reload is enabled - changes to code will auto-restart the server!"
