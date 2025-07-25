from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSettingsBase(BaseModel):
    profile_visibility: str = "public"
    email_visibility: bool = False
    phone_visibility: bool = False
    email_notifications: bool = True
    push_notifications: bool = True
    community_notifications: bool = True
    comment_notifications: bool = True
    mention_notifications: bool = True
    theme: str = "light"
    language: str = "en"
    timezone: str = "UTC"
    nsfw_content: bool = False
    auto_play_media: bool = True


class UserSettingsCreate(UserSettingsBase):
    user_id: int


class UserSettingsUpdate(BaseModel):
    profile_visibility: Optional[str] = None
    email_visibility: Optional[bool] = None
    phone_visibility: Optional[bool] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    community_notifications: Optional[bool] = None
    comment_notifications: Optional[bool] = None
    mention_notifications: Optional[bool] = None
    theme: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    nsfw_content: Optional[bool] = None
    auto_play_media: Optional[bool] = None


class UserSettingsResponse(UserSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SystemSettingsBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_public: bool = False


class SystemSettingsCreate(SystemSettingsBase):
    pass


class SystemSettingsUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_public: Optional[bool] = None


class SystemSettingsResponse(SystemSettingsBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationSettingsBase(BaseModel):
    notification_type: str
    category: str
    is_enabled: bool = True
    frequency: str = "immediate"


class NotificationSettingsCreate(NotificationSettingsBase):
    user_id: int


class NotificationSettingsUpdate(BaseModel):
    is_enabled: Optional[bool] = None
    frequency: Optional[str] = None


class NotificationSettingsResponse(NotificationSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
