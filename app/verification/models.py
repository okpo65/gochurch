from sqlalchemy import Column, String, DateTime, Text, ForeignKey, CheckConstraint, Integer
from sqlalchemy.sql import func
from database import Base


class IdentityVerification(Base):
    __tablename__ = "identity_verifications"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    photo_url = Column(Text, nullable=False)
    church_id = Column(Integer, ForeignKey("churches.id"))
    status = Column(String(20), nullable=False)
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'approved', 'rejected')", name='check_status'),
    )
