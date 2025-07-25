from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config.config import settings

# Create database engine with UUID support
engine = create_engine(settings.DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Legacy model for demonstration (keeping for backward compatibility)
class TaskResult(Base):
    __tablename__ = "task_results"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    task_type = Column(String)
    result = Column(Text)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Import all models to ensure they are registered with Base
from app.user.models import User, Profile
from app.church.models import Church
from app.verification.models import IdentityVerification
from app.community.models import Board, Post, PostTag, Comment
from app.action.models import ActionLog

# Create tables
def create_tables():
    # Enable UUID extension for PostgreSQL using proper SQLAlchemy syntax
    try:
        with engine.begin() as conn:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        print("✓ UUID extension enabled")
    except Exception as e:
        print(f"Note: UUID extension may already exist or not be needed: {e}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
