from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from . import schemas, service

router = APIRouter(prefix="/actions", tags=["action-logs"])


@router.post("/", response_model=schemas.ActionLogResponse)
def create_action_log(action_log: schemas.ActionLogCreate, db: Session = Depends(get_db)):
    return service.ActionLogService.create_action_log(db=db, action_log=action_log)


@router.post("/toggle", response_model=schemas.ActionLogResponse)
def toggle_action(
    user_id: int,
    action_type: str,
    target_type: str,
    target_id: int,
    db: Session = Depends(get_db)
):
    if action_type not in ["view", "like", "bookmark", "report"]:
        raise HTTPException(status_code=400, detail="Invalid action type")
    if target_type not in ["post", "comment"]:
        raise HTTPException(status_code=400, detail="Invalid target type")
    
    return service.ActionLogService.toggle_action(
        db=db,
        user_id=user_id,
        action_type=action_type,
        target_type=target_type,
        target_id=target_id
    )


@router.get("/user/{user_id}", response_model=List[schemas.ActionLogResponse])
def get_user_actions(
    user_id: int,
    action_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    actions = service.ActionLogService.get_user_actions(
        db, user_id=user_id, action_type=action_type, skip=skip, limit=limit
    )
    return actions


@router.get("/target/{target_type}/{target_id}", response_model=List[schemas.ActionLogResponse])
def get_target_actions(
    target_type: str,
    target_id: int,
    action_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if target_type not in ["post", "comment"]:
        raise HTTPException(status_code=400, detail="Invalid target type")
    
    actions = service.ActionLogService.get_target_actions(
        db, target_type=target_type, target_id=target_id, action_type=action_type, skip=skip, limit=limit
    )
    return actions


@router.get("/count/{target_type}/{target_id}/{action_type}")
def get_action_count(
    target_type: str,
    target_id: int,
    action_type: str,
    db: Session = Depends(get_db)
):
    if action_type not in ["view", "like", "bookmark", "report"]:
        raise HTTPException(status_code=400, detail="Invalid action type")
    if target_type not in ["post", "comment"]:
        raise HTTPException(status_code=400, detail="Invalid target type")
    
    count = service.ActionLogService.get_action_count(
        db, target_type=target_type, target_id=target_id, action_type=action_type
    )
    return {"count": count}


@router.get("/{action_log_id}", response_model=schemas.ActionLogResponse)
def get_action_log(action_log_id: int, db: Session = Depends(get_db)):
    db_action_log = service.ActionLogService.get_action_log(db, action_log_id=action_log_id)
    if db_action_log is None:
        raise HTTPException(status_code=404, detail="Action log not found")
    return db_action_log
