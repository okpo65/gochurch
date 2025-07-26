from sqlalchemy import Column, String, Text, Integer
from database import Base


class Church(Base):
    __tablename__ = "churches"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(Text, nullable=False)
    address = Column(Text)
    phone_number = Column(String(20))
