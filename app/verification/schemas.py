from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum


class VerificationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class IdentityVerificationBase(BaseModel):
    photo_url: str = Field(description="URL to the verification photo")
    church_id: Optional[uuid.UUID] = Field(None, description="UUID of the church for verification context")


class IdentityVerificationCreate(IdentityVerificationBase):
    user_id: uuid.UUID = Field(description="UUID of the user requesting verification")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "photo_url": "https://example.com/verification-photos/user123.jpg",
                "church_id": "550e8400-e29b-41d4-a716-446655440001"
            }
        }


class IdentityVerificationUpdate(BaseModel):
    status: VerificationStatus = Field(description="New verification status")
    reviewed_by: uuid.UUID = Field(description="UUID of the admin who reviewed this verification")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "approved",
                "reviewed_by": "550e8400-e29b-41d4-a716-446655440007"
            }
        }


class IdentityVerificationResponse(IdentityVerificationBase):
    id: uuid.UUID = Field(description="Unique identifier for the verification request")
    user_id: uuid.UUID = Field(description="UUID of the user who requested verification")
    status: VerificationStatus = Field(description="Current status of the verification")
    reviewed_by: Optional[uuid.UUID] = Field(None, description="UUID of the admin who reviewed this verification")
    created_at: datetime = Field(description="When the verification was requested")
    reviewed_at: Optional[datetime] = Field(None, description="When the verification was reviewed")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440008",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "photo_url": "https://example.com/verification-photos/user123.jpg",
                "church_id": "550e8400-e29b-41d4-a716-446655440001",
                "status": "pending",
                "reviewed_by": None,
                "created_at": "2024-01-15T09:00:00Z",
                "reviewed_at": None
            }
        }
