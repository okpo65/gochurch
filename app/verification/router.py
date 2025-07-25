from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from . import schemas, service
import uuid

router = APIRouter(prefix="/verifications", tags=["identity-verification"])


@router.post("/", response_model=schemas.IdentityVerificationResponse)
def create_verification(verification: schemas.IdentityVerificationCreate, db: Session = Depends(get_db)):
    return service.IdentityVerificationService.create_verification(db=db, verification=verification)


@router.get("/pending", response_model=List[schemas.IdentityVerificationResponse])
def get_pending_verifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    verifications = service.IdentityVerificationService.get_pending_verifications(db, skip=skip, limit=limit)
    return verifications


@router.get("/status/{status}", response_model=List[schemas.IdentityVerificationResponse])
def get_verifications_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if status not in ["pending", "approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    verifications = service.IdentityVerificationService.get_verifications_by_status(db, status=status, skip=skip, limit=limit)
    return verifications


@router.get("/user/{user_id}", response_model=List[schemas.IdentityVerificationResponse])
def get_user_verifications(user_id: uuid.UUID, db: Session = Depends(get_db)):
    verifications = service.IdentityVerificationService.get_verifications_by_user(db, user_id=user_id)
    return verifications


@router.get("/{verification_id}", response_model=schemas.IdentityVerificationResponse)
def get_verification(verification_id: uuid.UUID, db: Session = Depends(get_db)):
    db_verification = service.IdentityVerificationService.get_verification(db, verification_id=verification_id)
    if db_verification is None:
        raise HTTPException(status_code=404, detail="Verification not found")
    return db_verification


@router.put("/{verification_id}/status", response_model=schemas.IdentityVerificationResponse)
def update_verification_status(verification_id: uuid.UUID, verification_update: schemas.IdentityVerificationUpdate, db: Session = Depends(get_db)):
    db_verification = service.IdentityVerificationService.update_verification_status(db, verification_id=verification_id, verification_update=verification_update)
    if db_verification is None:
        raise HTTPException(status_code=404, detail="Verification not found")
    return db_verification
