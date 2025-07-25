from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas
import uuid


class UserService:
    @staticmethod
    def get_user(db: Session, user_id: uuid.UUID) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
        return db.query(models.User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate) -> models.User:
        db_user = models.User(
            is_blocked=user.is_blocked,
            is_admin=user.is_admin
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: uuid.UUID, user_update: schemas.UserUpdate) -> Optional[models.User]:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user:
            update_data = user_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_user, field, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: uuid.UUID) -> bool:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False


class ProfileService:
    @staticmethod
    def get_profile(db: Session, profile_id: uuid.UUID) -> Optional[models.Profile]:
        return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

    @staticmethod
    def get_profile_by_user(db: Session, user_id: uuid.UUID) -> Optional[models.Profile]:
        return db.query(models.Profile).filter(models.Profile.user_id == user_id).first()

    @staticmethod
    def create_profile(db: Session, profile: schemas.ProfileCreate) -> models.Profile:
        db_profile = models.Profile(
            user_id=profile.user_id,
            nickname=profile.nickname,
            thumbnail=profile.thumbnail,
            church_id=profile.church_id
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    @staticmethod
    def update_profile(db: Session, profile_id: uuid.UUID, profile_update: schemas.ProfileUpdate) -> Optional[models.Profile]:
        db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
        if db_profile:
            update_data = profile_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_profile, field, value)
            db.commit()
            db.refresh(db_profile)
        return db_profile

    @staticmethod
    def delete_profile(db: Session, profile_id: uuid.UUID) -> bool:
        db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
        if db_profile:
            db.delete(db_profile)
            db.commit()
            return True
        return False
