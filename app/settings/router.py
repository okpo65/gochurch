from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from database import get_db
from app.signin.router import get_current_user
from . import schemas, service

router = APIRouter(prefix="/settings", tags=["settings"])


# User Settings endpoints
@router.get("/user", response_model=schemas.UserSettingsResponse)
def get_user_settings(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    settings = service.UserSettingsService.get_or_create_user_settings(db, current_user.id)
    return settings


@router.put("/user", response_model=schemas.UserSettingsResponse)
def update_user_settings(
    settings_update: schemas.UserSettingsUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    settings = service.UserSettingsService.update_user_settings(db, current_user.id, settings_update)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings


# System Settings endpoints (admin only - you might want to add admin check)
@router.get("/system", response_model=List[schemas.SystemSettingsResponse])
def get_system_settings(
    category: str = None,
    public_only: bool = True,
    db: Session = Depends(get_db)
):
    settings = service.SystemSettingsService.get_system_settings(db, category=category, public_only=public_only)
    return settings


@router.get("/system/public")
def get_public_system_settings(db: Session = Depends(get_db)) -> Dict[str, Any]:
    return service.SystemSettingsService.get_public_settings_dict(db)


@router.post("/system", response_model=schemas.SystemSettingsResponse)
def create_system_setting(
    setting: schemas.SystemSettingsCreate,
    db: Session = Depends(get_db)
    # Add admin authentication here
):
    # Check if setting already exists
    existing_setting = service.SystemSettingsService.get_system_setting(db, setting.key)
    if existing_setting:
        raise HTTPException(status_code=400, detail="Setting with this key already exists")
    
    return service.SystemSettingsService.create_system_setting(db, setting)


@router.put("/system/{key}", response_model=schemas.SystemSettingsResponse)
def update_system_setting(
    key: str,
    setting_update: schemas.SystemSettingsUpdate,
    db: Session = Depends(get_db)
    # Add admin authentication here
):
    setting = service.SystemSettingsService.update_system_setting(db, key, setting_update)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.delete("/system/{key}")
def delete_system_setting(
    key: str,
    db: Session = Depends(get_db)
    # Add admin authentication here
):
    success = service.SystemSettingsService.delete_system_setting(db, key)
    if not success:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"message": "Setting deleted successfully"}


# Notification Settings endpoints
@router.get("/notifications", response_model=List[schemas.NotificationSettingsResponse])
def get_notification_settings(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    settings = service.NotificationSettingsService.get_notification_settings(db, current_user.id)
    return settings


@router.post("/notifications", response_model=schemas.NotificationSettingsResponse)
def create_notification_setting(
    setting: schemas.NotificationSettingsCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure the setting is for the current user
    setting.user_id = current_user.id
    
    # Check if setting already exists
    existing_setting = service.NotificationSettingsService.get_notification_setting(
        db, current_user.id, setting.notification_type, setting.category
    )
    if existing_setting:
        raise HTTPException(status_code=400, detail="Notification setting already exists")
    
    return service.NotificationSettingsService.create_notification_setting(db, setting)


@router.put("/notifications/{notification_type}/{category}", response_model=schemas.NotificationSettingsResponse)
def update_notification_setting(
    notification_type: str,
    category: str,
    setting_update: schemas.NotificationSettingsUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    setting = service.NotificationSettingsService.update_notification_setting(
        db, current_user.id, notification_type, category, setting_update
    )
    if not setting:
        raise HTTPException(status_code=404, detail="Notification setting not found")
    return setting


@router.post("/notifications/defaults")
def create_default_notification_settings(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service.NotificationSettingsService.create_default_notification_settings(db, current_user.id)
    return {"message": "Default notification settings created successfully"}
