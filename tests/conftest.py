import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from config.config import settings

# Test database configuration with separate port
def get_test_database_url():
    """Generate test database URL with separate port for isolation"""
    return settings.get_test_database_url()

def get_postgres_url_for_test_db():
    """Get postgres database URL for test database server"""
    test_url = get_test_database_url()
    # Replace database name with 'postgres' for administrative operations
    parts = test_url.rsplit("/", 1)
    return f"{parts[0]}/postgres"

TEST_DATABASE_URL = get_test_database_url()

# Create test engine with proper configuration
test_engine = create_engine(
    TEST_DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,
    pool_recycle=300
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    """Override database dependency for tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

def create_test_database_if_not_exists():
    """Create test database if it doesn't exist"""
    postgres_url = get_postgres_url_for_test_db()
    db_name = settings.TEST_DB_NAME
    
    try:
        # Connect to postgres database on test port
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            conn = conn.execution_options(autocommit=True)
            
            # Check if database exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            if not result.fetchone():
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                print(f"✅ Created test database: {db_name} on port {settings.TEST_DB_PORT}")
            else:
                print(f"✅ Test database already exists: {db_name} on port {settings.TEST_DB_PORT}")
        
        engine.dispose()
        return True
    except Exception as e:
        print(f"❌ Failed to create test database: {e}")
        print(f"   Make sure PostgreSQL is running on port {settings.TEST_DB_PORT}")
        print(f"   You may need to start a separate PostgreSQL instance for testing")
        return False

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Setup test database with UUID extension and tables"""
    print(f"\n🔧 Setting up test database: {TEST_DATABASE_URL}")
    print(f"   Main DB Port: {settings.DB_PORT}")
    print(f"   Test DB Port: {settings.TEST_DB_PORT}")
    
    # Create test database if it doesn't exist
    if not create_test_database_if_not_exists():
        pytest.exit("Failed to create test database. Please check your test database configuration.")
    
    # Enable UUID extension
    try:
        with test_engine.begin() as conn:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        print("✅ UUID extension enabled")
    except Exception as e:
        print(f"⚠️  UUID extension note: {e}")
    
    # Create all tables
    try:
        Base.metadata.create_all(bind=test_engine)
        print("✅ Test database tables created")
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        pytest.exit("Failed to create test database tables")
    
    yield
    
    # Cleanup after all tests
    print(f"\n🧹 Cleaning up test database on port {settings.TEST_DB_PORT}")
    try:
        Base.metadata.drop_all(bind=test_engine)
        print("✅ Test database cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

@pytest.fixture
def client():
    """Create test client"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def db_session():
    """Create database session for tests with transaction rollback"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def clean_db_session():
    """Create a clean database session that commits changes (use sparingly)"""
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Test data fixtures
@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
    }

@pytest.fixture
def sample_church_data():
    """Sample church data for testing"""
    return {
        "name": "Test Church",
        "address": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "zip_code": "12345",
        "phone": "555-0123",
        "email": "info@testchurch.com"
    }

@pytest.fixture
def sample_board_data():
    """Sample board data for testing"""
    return {
        "name": "Test Board",
        "description": "A test discussion board"
    }
