from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid


class Church(Base):
    __tablename__ = "churches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(Text, nullable=False)
    address = Column(Text)
    phone_number = Column(String(20))
