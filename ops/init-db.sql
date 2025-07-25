-- Initialize database for FastAPI Celery application
-- This script runs when PostgreSQL container starts for the first time

-- Create the database (already created by POSTGRES_DB env var)
-- CREATE DATABASE fastapi_celery_db;

-- Grant permissions to the user (already handled by POSTGRES_USER env var)
-- GRANT ALL PRIVILEGES ON DATABASE fastapi_celery_db TO fastapi_user;

-- You can add any additional database setup here
-- For example, extensions, initial data, etc.

-- Enable UUID extension if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

SELECT 'Database initialized successfully' as message;
