#!/bin/bash

echo "Setting up FastAPI + Celery + PostgreSQL environment..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Error: Homebrew is not installed. Please install Homebrew first."
    echo "Visit: https://brew.sh/"
    exit 1
fi

# Install PostgreSQL
echo "Installing PostgreSQL..."
brew install postgresql
brew services start postgresql

# Install Redis (if not already installed)
echo "Installing Redis..."
brew install redis
brew services start redis

# Wait for services to start
sleep 3

# Create PostgreSQL user and database
echo "Setting up PostgreSQL database..."
createuser -s $(whoami) 2>/dev/null || echo "User already exists"
createdb fastapi_celery_db 2>/dev/null || echo "Database already exists"

# Setup database using our script
echo "Running database setup..."
poetry run python setup_db.py

# Create initial migration
echo "Creating database migration..."
poetry run alembic revision --autogenerate -m "Initial migration"

# Run migrations
echo "Running database migrations..."
poetry run alembic upgrade head

echo ""
echo "Environment setup complete!"
echo "You can now run: ./start.sh"
