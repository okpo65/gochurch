from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas
import uuid


class IdentityVerificationService:
    @staticmethod
    def create_verification(db: Session, verification: schemas.IdentityVerificationCreate) -> models.IdentityVerification:
        db_verification = models.IdentityVerification(
            user_id=verification.user_id,
            photo_url=verification.photo_url,
            church_id=verification.church_id,
            status="pending"
        )
        db.add(db_verification)
        db.commit()
        db.refresh(db_verification)
        return db_verification

    @staticmethod
    def get_verification(db: Session, verification_id: uuid.UUID) -> Optional[models.IdentityVerification]:
        return db.query(models.IdentityVerification).filter(models.IdentityVerification.id == verification_id).first()

    @staticmethod
    def get_verifications_by_user(db: Session, user_id: uuid.UUID) -> List[models.IdentityVerification]:
        return db.query(models.IdentityVerification).filter(models.IdentityVerification.user_id == user_id).all()

    @staticmethod
    def get_pending_verifications(db: Session, skip: int = 0, limit: int = 100) -> List[models.IdentityVerification]:
        return db.query(models.IdentityVerification).filter(
            models.IdentityVerification.status == "pending"
        ).offset(skip).limit(limit).all()

    @staticmethod
    def update_verification_status(db: Session, verification_id: uuid.UUID, verification_update: schemas.IdentityVerificationUpdate) -> Optional[models.IdentityVerification]:
        db_verification = db.query(models.IdentityVerification).filter(models.IdentityVerification.id == verification_id).first()
        if db_verification:
            db_verification.status = verification_update.status
            db_verification.reviewed_by = verification_update.reviewed_by
            from sqlalchemy.sql import func
            db_verification.reviewed_at = func.now()
            db.commit()
            db.refresh(db_verification)
        return db_verification

    @staticmethod
    def get_verifications_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[models.IdentityVerification]:
        return db.query(models.IdentityVerification).filter(
            models.IdentityVerification.status == status
        ).offset(skip).limit(limit).all()
