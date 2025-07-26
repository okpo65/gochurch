-- Initialize UUID extension for PostgreSQL
-- This script runs automatically when the PostgreSQL container starts

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create additional extensions that might be useful
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Log the initialization
DO $$
BEGIN
    RAISE NOTICE 'GoChurch Database Initialized with UUID support';
END $$;
