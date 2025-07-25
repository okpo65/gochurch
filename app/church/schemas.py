from pydantic import BaseModel, Field
from typing import Optional
import uuid


class ChurchBase(BaseModel):
    name: str = Field(description="Name of the church", max_length=200)
    address: Optional[str] = Field(None, description="Physical address of the church")
    phone_number: Optional[str] = Field(None, max_length=20, description="Contact phone number")


class ChurchCreate(ChurchBase):
    class Config:
        schema_extra = {
            "example": {
                "name": "First Baptist Church",
                "address": "123 Main Street, Anytown, USA 12345",
                "phone_number": "+1-555-0123"
            }
        }


class ChurchUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the church", max_length=200)
    address: Optional[str] = Field(None, description="Physical address of the church")
    phone_number: Optional[str] = Field(None, max_length=20, description="Contact phone number")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "First Baptist Church - Updated",
                "address": "456 New Street, Anytown, USA 12345",
                "phone_number": "+1-555-0456"
            }
        }


class ChurchResponse(ChurchBase):
    id: uuid.UUID = Field(description="Unique identifier for the church")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "First Baptist Church",
                "address": "123 Main Street, Anytown, USA 12345",
                "phone_number": "+1-555-0123"
            }
        }
