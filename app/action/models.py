from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, CheckConstraint, Index, Integer
from sqlalchemy.sql import func
from database import Base


class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type = Column(String(50), nullable=False)
    target_type = Column(String(50), nullable=False)
    target_id = Column(Integer, nullable=False)
    is_on = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint("action_type IN ('view', 'like', 'bookmark', 'report')", name='check_action_type'),
        CheckConstraint("target_type IN ('post', 'comment')", name='check_target_type'),
        Index('idx_action_logs_target', 'target_type', 'target_id'),
    )
