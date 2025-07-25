from sqlalchemy import Column, String, DateTime, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid


class IdentityVerification(Base):
    __tablename__ = "identity_verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    photo_url = Column(Text, nullable=False)
    church_id = Column(UUID(as_uuid=True), ForeignKey("churches.id"))
    status = Column(String(20), nullable=False)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'approved', 'rejected')", name='check_status'),
    )
