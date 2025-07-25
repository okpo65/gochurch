from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.user.service import UserService
from app.user.models import User
from . import schemas
import os

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, credentials_exception):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            if username is None or user_id is None:
                raise credentials_exception
            token_data = schemas.TokenData(username=username, user_id=user_id)
        except JWTError:
            raise credentials_exception
        return token_data

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not UserService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def login(db: Session, login_request: schemas.LoginRequest) -> schemas.LoginResponse:
        user = AuthService.authenticate_user(db, login_request.email, login_request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(
            data={"sub": user.username, "user_id": user.id}, 
            expires_delta=access_token_expires
        )
        
        return schemas.LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            username=user.username,
            email=user.email
        )

    @staticmethod
    def change_password(db: Session, user_id: int, change_request: schemas.ChangePasswordRequest) -> bool:
        user = UserService.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not UserService.verify_password(change_request.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password"
            )
        
        # Update password
        user.hashed_password = UserService.get_password_hash(change_request.new_password)
        db.commit()
        return True

    @staticmethod
    def request_password_reset(db: Session, email: str) -> bool:
        user = UserService.get_user_by_email(db, email)
        if not user:
            # Don't reveal if email exists or not
            return True
        
        # Generate reset token (in production, send via email)
        reset_token = AuthService.create_access_token(
            data={"sub": user.username, "user_id": user.id, "reset": True},
            expires_delta=timedelta(hours=1)
        )
        
        # In production, you would send this token via email
        # For now, we'll just return True
        print(f"Password reset token for {email}: {reset_token}")
        return True

    @staticmethod
    def reset_password(db: Session, reset_request: schemas.PasswordResetConfirm) -> bool:
        try:
            payload = jwt.decode(reset_request.token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            is_reset: bool = payload.get("reset", False)
            
            if not username or not user_id or not is_reset:
                raise HTTPException(status_code=400, detail="Invalid reset token")
            
            user = UserService.get_user(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Update password
            user.hashed_password = UserService.get_password_hash(reset_request.new_password)
            db.commit()
            return True
            
        except JWTError:
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")
