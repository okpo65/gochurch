from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    # Use Python's uuid.uuid4 as default instead of PostgreSQL's uuid_generate_v4()
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    is_blocked = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)


class Profile(Base):
    __tablename__ = "profiles"

    # Use Python's uuid.uuid4 as default instead of PostgreSQL's uuid_generate_v4()
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    nickname = Column(String(100))
    thumbnail = Column(Text)
    church_id = Column(UUID(as_uuid=True), ForeignKey("churches.id"))
