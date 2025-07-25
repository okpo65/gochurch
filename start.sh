#!/bin/bash

echo "🚀 Starting GoChurch Community Server..."

# Check if we're in the right directory
if [ ! -f ".python-version" ]; then
    echo "❌ Error: .python-version file not found. Make sure you're in the project directory."
    exit 1
fi

# Check if Poetry is available
if ! command -v poetry &> /dev/null; then
    echo "❌ Error: Poetry is not installed. Please install Poetry first."
    exit 1
fi

# Make sure Redis is running
echo "📋 Prerequisites:"
echo "   - Redis should be running on localhost:6379"
echo "   - PostgreSQL should be running with database configured"
echo "   - Run 'python scripts/setup_db.py' if database isn't set up"

echo ""
echo "🔄 Starting Celery worker..."
# Start Celery worker in background using Poetry
poetry run celery -A workers.celery_app worker --loglevel=info &

# Store the Celery process ID
CELERY_PID=$!

# Wait a moment for Celery to start
sleep 3

echo "🌐 Starting FastAPI server..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "📚 ReDoc Documentation: http://localhost:8000/redoc"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start FastAPI server using Poetry
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# When FastAPI stops, also stop Celery
echo "🛑 Stopping Celery worker..."
kill $CELERY_PID 2>/dev/null
