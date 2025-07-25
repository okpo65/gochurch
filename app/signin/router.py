from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from app.user.service import UserService
from . import schemas, service

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = service.AuthService.verify_token(credentials.credentials, credentials_exception)
    user = UserService.get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


@router.post("/login", response_model=schemas.LoginResponse)
def login(login_request: schemas.LoginRequest, db: Session = Depends(get_db)):
    return service.AuthService.login(db, login_request)


@router.post("/logout")
def logout():
    # In a real application, you might want to blacklist the token
    return {"message": "Successfully logged out"}


@router.post("/change-password")
def change_password(
    change_request: schemas.ChangePasswordRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = service.AuthService.change_password(db, current_user.id, change_request)
    if success:
        return {"message": "Password changed successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to change password")


@router.post("/forgot-password")
def request_password_reset(reset_request: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    service.AuthService.request_password_reset(db, reset_request.email)
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password")
def reset_password(reset_request: schemas.PasswordResetConfirm, db: Session = Depends(get_db)):
    success = service.AuthService.reset_password(db, reset_request)
    if success:
        return {"message": "Password reset successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to reset password")


@router.get("/me")
def get_current_user_info(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified
    }
