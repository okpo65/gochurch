from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum


class ActionType(str, Enum):
    VIEW = "view"
    LIKE = "like"
    BOOKMARK = "bookmark"
    REPORT = "report"


class TargetType(str, Enum):
    POST = "post"
    COMMENT = "comment"


class ActionLogBase(BaseModel):
    action_type: ActionType = Field(description="Type of action performed")
    target_type: TargetType = Field(description="Type of target (post or comment)")
    target_id: uuid.UUID = Field(description="UUID of the target item")
    is_on: bool = Field(default=True, description="Whether the action is active (true) or inactive (false)")


class ActionLogCreate(ActionLogBase):
    user_id: uuid.UUID = Field(description="UUID of the user performing the action")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "action_type": "like",
                "target_type": "post",
                "target_id": "550e8400-e29b-41d4-a716-446655440004",
                "is_on": True
            }
        }


class ActionLogUpdate(BaseModel):
    is_on: Optional[bool] = Field(None, description="Whether the action is active (true) or inactive (false)")
    
    class Config:
        schema_extra = {
            "example": {
                "is_on": False
            }
        }


class ActionLogResponse(ActionLogBase):
    id: uuid.UUID = Field(description="Unique identifier for the action log")
    user_id: uuid.UUID = Field(description="UUID of the user who performed the action")
    created_at: datetime = Field(description="When the action was performed")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440006",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "action_type": "like",
                "target_type": "post",
                "target_id": "550e8400-e29b-41d4-a716-446655440004",
                "is_on": True,
                "created_at": "2024-01-15T12:00:00Z"
            }
        }
