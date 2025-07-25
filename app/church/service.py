from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas
import uuid


class ChurchService:
    @staticmethod
    def create_church(db: Session, church: schemas.ChurchCreate) -> models.Church:
        db_church = models.Church(
            name=church.name,
            address=church.address,
            phone_number=church.phone_number
        )
        db.add(db_church)
        db.commit()
        db.refresh(db_church)
        return db_church

    @staticmethod
    def get_church(db: Session, church_id: uuid.UUID) -> Optional[models.Church]:
        return db.query(models.Church).filter(models.Church.id == church_id).first()

    @staticmethod
    def get_churches(db: Session, skip: int = 0, limit: int = 100) -> List[models.Church]:
        return db.query(models.Church).offset(skip).limit(limit).all()

    @staticmethod
    def update_church(db: Session, church_id: uuid.UUID, church_update: schemas.ChurchUpdate) -> Optional[models.Church]:
        db_church = db.query(models.Church).filter(models.Church.id == church_id).first()
        if db_church:
            update_data = church_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_church, field, value)
            db.commit()
            db.refresh(db_church)
        return db_church

    @staticmethod
    def delete_church(db: Session, church_id: uuid.UUID) -> bool:
        db_church = db.query(models.Church).filter(models.Church.id == church_id).first()
        if db_church:
            db.delete(db_church)
            db.commit()
            return True
        return False
