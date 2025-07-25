from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from . import models, schemas


class UserSettingsService:
    @staticmethod
    def get_user_settings(db: Session, user_id: int) -> Optional[models.UserSettings]:
        return db.query(models.UserSettings).filter(models.UserSettings.user_id == user_id).first()

    @staticmethod
    def create_user_settings(db: Session, user_id: int) -> models.UserSettings:
        # Check if settings already exist
        existing_settings = UserSettingsService.get_user_settings(db, user_id)
        if existing_settings:
            return existing_settings
        
        db_settings = models.UserSettings(user_id=user_id)
        db.add(db_settings)
        db.commit()
        db.refresh(db_settings)
        return db_settings

    @staticmethod
    def update_user_settings(db: Session, user_id: int, settings_update: schemas.UserSettingsUpdate) -> Optional[models.UserSettings]:
        db_settings = UserSettingsService.get_user_settings(db, user_id)
        if not db_settings:
            # Create default settings if they don't exist
            db_settings = UserSettingsService.create_user_settings(db, user_id)
        
        update_data = settings_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_settings, field, value)
        
        db.commit()
        db.refresh(db_settings)
        return db_settings

    @staticmethod
    def get_or_create_user_settings(db: Session, user_id: int) -> models.UserSettings:
        settings = UserSettingsService.get_user_settings(db, user_id)
        if not settings:
            settings = UserSettingsService.create_user_settings(db, user_id)
        return settings


class SystemSettingsService:
    @staticmethod
    def get_system_setting(db: Session, key: str) -> Optional[models.SystemSettings]:
        return db.query(models.SystemSettings).filter(models.SystemSettings.key == key).first()

    @staticmethod
    def get_system_settings(db: Session, category: Optional[str] = None, public_only: bool = False) -> List[models.SystemSettings]:
        query = db.query(models.SystemSettings)
        
        if category:
            query = query.filter(models.SystemSettings.category == category)
        
        if public_only:
            query = query.filter(models.SystemSettings.is_public == True)
        
        return query.all()

    @staticmethod
    def create_system_setting(db: Session, setting: schemas.SystemSettingsCreate) -> models.SystemSettings:
        db_setting = models.SystemSettings(
            key=setting.key,
            value=setting.value,
            description=setting.description,
            category=setting.category,
            is_public=setting.is_public
        )
        db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
        return db_setting

    @staticmethod
    def update_system_setting(db: Session, key: str, setting_update: schemas.SystemSettingsUpdate) -> Optional[models.SystemSettings]:
        db_setting = SystemSettingsService.get_system_setting(db, key)
        if db_setting:
            update_data = setting_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_setting, field, value)
            db.commit()
            db.refresh(db_setting)
        return db_setting

    @staticmethod
    def delete_system_setting(db: Session, key: str) -> bool:
        db_setting = SystemSettingsService.get_system_setting(db, key)
        if db_setting:
            db.delete(db_setting)
            db.commit()
            return True
        return False

    @staticmethod
    def get_public_settings_dict(db: Session) -> Dict[str, Any]:
        """Get all public system settings as a dictionary"""
        settings = SystemSettingsService.get_system_settings(db, public_only=True)
        return {setting.key: setting.value for setting in settings}


class NotificationSettingsService:
    @staticmethod
    def get_notification_settings(db: Session, user_id: int) -> List[models.NotificationSettings]:
        return db.query(models.NotificationSettings).filter(models.NotificationSettings.user_id == user_id).all()

    @staticmethod
    def get_notification_setting(db: Session, user_id: int, notification_type: str, category: str) -> Optional[models.NotificationSettings]:
        return db.query(models.NotificationSettings).filter(
            models.NotificationSettings.user_id == user_id,
            models.NotificationSettings.notification_type == notification_type,
            models.NotificationSettings.category == category
        ).first()

    @staticmethod
    def create_notification_setting(db: Session, setting: schemas.NotificationSettingsCreate) -> models.NotificationSettings:
        db_setting = models.NotificationSettings(
            user_id=setting.user_id,
            notification_type=setting.notification_type,
            category=setting.category,
            is_enabled=setting.is_enabled,
            frequency=setting.frequency
        )
        db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
        return db_setting

    @staticmethod
    def update_notification_setting(db: Session, user_id: int, notification_type: str, category: str, setting_update: schemas.NotificationSettingsUpdate) -> Optional[models.NotificationSettings]:
        db_setting = NotificationSettingsService.get_notification_setting(db, user_id, notification_type, category)
        if db_setting:
            update_data = setting_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_setting, field, value)
            db.commit()
            db.refresh(db_setting)
        return db_setting

    @staticmethod
    def create_default_notification_settings(db: Session, user_id: int):
        """Create default notification settings for a new user"""
        default_settings = [
            {"notification_type": "email", "category": "community", "is_enabled": True, "frequency": "immediate"},
            {"notification_type": "email", "category": "comment", "is_enabled": True, "frequency": "immediate"},
            {"notification_type": "email", "category": "mention", "is_enabled": True, "frequency": "immediate"},
            {"notification_type": "push", "category": "community", "is_enabled": True, "frequency": "immediate"},
            {"notification_type": "push", "category": "comment", "is_enabled": True, "frequency": "immediate"},
            {"notification_type": "push", "category": "mention", "is_enabled": True, "frequency": "immediate"},
        ]
        
        for setting_data in default_settings:
            setting = schemas.NotificationSettingsCreate(
                user_id=user_id,
                **setting_data
            )
            NotificationSettingsService.create_notification_setting(db, setting)
