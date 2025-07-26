import os
from dotenv import load_dotenv


import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(project_root, ".env"))

class Settings:
    # Main Database settings
    
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "fastapi_celery_db")
    DB_USER: str = os.getenv("DB_USER", "username")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")

    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Test Database settings (separate port for isolation)
    
    TEST_DB_HOST: str = os.getenv("TEST_DB_HOST", "localhost")
    TEST_DB_PORT: int = int(os.getenv("TEST_DB_PORT", "5433"))  # Different port for test DB
    TEST_DB_NAME: str = os.getenv("TEST_DB_NAME", "test_fastapi_celery_db")
    TEST_DB_USER: str = os.getenv("TEST_DB_USER", os.getenv("DB_USER", "username"))
    TEST_DB_PASSWORD: str = os.getenv("TEST_DB_PASSWORD", os.getenv("DB_PASSWORD", "password"))
    
    TEST_DATABASE_URL: str = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Test Redis settings (separate DB for isolation)
    TEST_REDIS_URL: str = os.getenv("TEST_REDIS_URL", "redis://localhost:6379/1")  # Different DB number
    TEST_REDIS_DB: int = int(os.getenv("TEST_REDIS_DB", "1"))
    
    # Application settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Testing settings
    TESTING: bool = os.getenv("TESTING", "False").lower() == "true"
    
    # Celery settings
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    def get_test_database_url(self) -> str:
        """Generate test database URL with separate port"""
        if self.TEST_DATABASE_URL:
            return self.TEST_DATABASE_URL
        
        return f"postgresql://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

settings = Settings()
