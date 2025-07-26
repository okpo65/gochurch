from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    is_blocked: bool = Field(default=False, description="Whether the user is blocked from the system")
    is_admin: bool = Field(default=False, description="Whether the user has administrative privileges")


class UserCreate(UserBase):
    class Config:
        schema_extra = {
            "example": {
                "is_blocked": False,
                "is_admin": False
            }
        }


class UserUpdate(BaseModel):
    is_blocked: Optional[bool] = Field(None, description="Whether the user is blocked from the system")
    is_admin: Optional[bool] = Field(None, description="Whether the user has administrative privileges")
    
    class Config:
        schema_extra = {
            "example": {
                "is_blocked": False,
                "is_admin": True
            }
        }


class UserResponse(UserBase):
    id: int = Field(description="Unique identifier for the user")
    created_at: datetime = Field(description="When the user was created")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "is_blocked": False,
                "is_admin": False,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


class ProfileBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=100, description="Display name for the user")
    thumbnail: Optional[str] = Field(None, description="URL to the user's profile image")
    church_id: Optional[int] = Field(None, description="ID of the church this user belongs to")


class ProfileCreate(ProfileBase):
    user_id: int = Field(description="ID of the user this profile belongs to")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "nickname": "john_doe",
                "thumbnail": "https://example.com/avatars/john.jpg",
                "church_id": 2
            }
        }


class ProfileUpdate(ProfileBase):
    class Config:
        schema_extra = {
            "example": {
                "nickname": "john_updated",
                "thumbnail": "https://example.com/avatars/john_new.jpg"
            }
        }


class ProfileResponse(ProfileBase):
    id: int = Field(description="Unique identifier for the profile")
    user_id: int = Field(description="ID of the user this profile belongs to")
    created_at: datetime = Field(description="When the profile was created")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "nickname": "john_doe",
                "thumbnail": "https://example.com/avatars/john.jpg",
                "church_id": 2,
                "created_at": "2024-01-15T10:35:00Z"
            }
        }
