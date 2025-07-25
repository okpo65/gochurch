from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas
import uuid


class ActionLogService:
    @staticmethod
    def create_action_log(db: Session, action_log: schemas.ActionLogCreate) -> models.ActionLog:
        # Check if action already exists for this user and target
        existing_action = db.query(models.ActionLog).filter(
            models.ActionLog.user_id == action_log.user_id,
            models.ActionLog.action_type == action_log.action_type,
            models.ActionLog.target_type == action_log.target_type,
            models.ActionLog.target_id == action_log.target_id
        ).first()
        
        if existing_action:
            # Update existing action
            existing_action.is_on = action_log.is_on
            from sqlalchemy.sql import func
            existing_action.created_at = func.now()
            db.commit()
            db.refresh(existing_action)
            return existing_action
        else:
            # Create new action
            db_action_log = models.ActionLog(
                user_id=action_log.user_id,
                action_type=action_log.action_type,
                target_type=action_log.target_type,
                target_id=action_log.target_id,
                is_on=action_log.is_on
            )
            db.add(db_action_log)
            db.commit()
            db.refresh(db_action_log)
            return db_action_log

    @staticmethod
    def get_action_log(db: Session, action_log_id: uuid.UUID) -> Optional[models.ActionLog]:
        return db.query(models.ActionLog).filter(models.ActionLog.id == action_log_id).first()

    @staticmethod
    def get_user_actions(db: Session, user_id: uuid.UUID, action_type: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[models.ActionLog]:
        query = db.query(models.ActionLog).filter(models.ActionLog.user_id == user_id)
        if action_type:
            query = query.filter(models.ActionLog.action_type == action_type)
        return query.order_by(models.ActionLog.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_target_actions(db: Session, target_type: str, target_id: uuid.UUID, action_type: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[models.ActionLog]:
        query = db.query(models.ActionLog).filter(
            models.ActionLog.target_type == target_type,
            models.ActionLog.target_id == target_id
        )
        if action_type:
            query = query.filter(models.ActionLog.action_type == action_type)
        return query.order_by(models.ActionLog.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def toggle_action(db: Session, user_id: uuid.UUID, action_type: str, target_type: str, target_id: uuid.UUID) -> models.ActionLog:
        existing_action = db.query(models.ActionLog).filter(
            models.ActionLog.user_id == user_id,
            models.ActionLog.action_type == action_type,
            models.ActionLog.target_type == target_type,
            models.ActionLog.target_id == target_id
        ).first()
        
        if existing_action:
            existing_action.is_on = not existing_action.is_on
            from sqlalchemy.sql import func
            existing_action.created_at = func.now()
            db.commit()
            db.refresh(existing_action)
            return existing_action
        else:
            action_log = schemas.ActionLogCreate(
                user_id=user_id,
                action_type=action_type,
                target_type=target_type,
                target_id=target_id,
                is_on=True
            )
            return ActionLogService.create_action_log(db, action_log)

    @staticmethod
    def get_action_count(db: Session, target_type: str, target_id: uuid.UUID, action_type: str) -> int:
        return db.query(models.ActionLog).filter(
            models.ActionLog.target_type == target_type,
            models.ActionLog.target_id == target_id,
            models.ActionLog.action_type == action_type,
            models.ActionLog.is_on == True
        ).count()
