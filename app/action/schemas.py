from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
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
    target_id: int = Field(description="ID of the target item")
    is_on: bool = Field(default=True, description="Whether the action is active (true) or inactive (false)")


class ActionLogCreate(ActionLogBase):
    user_id: int = Field(description="ID of the user performing the action")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "action_type": "like",
                "target_type": "post",
                "target_id": 1,
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
    id: int = Field(description="Unique identifier for the action log")
    user_id: int = Field(description="ID of the user who performed the action")
    created_at: datetime = Field(description="When the action was performed")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "action_type": "like",
                "target_type": "post",
                "target_id": 1,
                "is_on": True,
                "created_at": "2024-01-15T12:00:00Z"
            }
        }
