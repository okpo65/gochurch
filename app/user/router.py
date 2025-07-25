from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from . import schemas, service
import uuid

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", 
             response_model=schemas.UserResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new user",
             description="""
Create a new user in the system.

- **is_blocked**: Whether the user is blocked (default: false)
- **is_admin**: Whether the user has admin privileges (default: false)

Returns the created user with a generated UUID.
             """,
             response_description="The created user information")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.UserService.create_user(db=db, user=user)


@router.get("/", 
            response_model=List[schemas.UserResponse],
            summary="List all users",
            description="""
Retrieve a paginated list of all users in the system.

- **skip**: Number of users to skip (for pagination)
- **limit**: Maximum number of users to return (max 100)
            """,
            response_description="List of users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = service.UserService.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", 
            response_model=schemas.UserResponse,
            summary="Get user by ID",
            description="""
Retrieve a specific user by their UUID.

- **user_id**: The UUID of the user to retrieve

Example UUID: `550e8400-e29b-41d4-a716-446655440000`
            """,
            response_description="The requested user information",
            responses={
                404: {"description": "User not found"}
            })
def read_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = service.UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", 
            response_model=schemas.UserResponse,
            summary="Update user",
            description="""
Update an existing user's information.

- **user_id**: The UUID of the user to update
- Only provided fields will be updated (partial updates supported)
            """,
            response_description="The updated user information",
            responses={
                404: {"description": "User not found"}
            })
def update_user(user_id: uuid.UUID, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = service.UserService.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}",
               status_code=status.HTTP_200_OK,
               summary="Delete user",
               description="""
Delete a user from the system.

⚠️ **Warning**: This will also delete all associated data (profiles, posts, comments, etc.) due to CASCADE constraints.

- **user_id**: The UUID of the user to delete
               """,
               response_description="Confirmation message",
               responses={
                   404: {"description": "User not found"}
               })
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    success = service.UserService.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


# Profile endpoints
@router.post("/profiles/", 
             response_model=schemas.ProfileResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create user profile",
             description="""
Create a profile for an existing user.

- **user_id**: UUID of the user this profile belongs to
- **nickname**: Display name for the user (optional)
- **thumbnail**: URL to profile image (optional)
- **church_id**: UUID of the church this user belongs to (optional)

Each user can have only one profile.
             """,
             response_description="The created profile information")
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return service.ProfileService.create_profile(db=db, profile=profile)


@router.get("/profiles/{profile_id}", 
            response_model=schemas.ProfileResponse,
            summary="Get profile by ID",
            description="""
Retrieve a specific profile by its UUID.

- **profile_id**: The UUID of the profile to retrieve
            """,
            response_description="The requested profile information",
            responses={
                404: {"description": "Profile not found"}
            })
def read_profile(profile_id: uuid.UUID, db: Session = Depends(get_db)):
    db_profile = service.ProfileService.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@router.get("/{user_id}/profile", 
            response_model=schemas.ProfileResponse,
            summary="Get user's profile",
            description="""
Retrieve the profile for a specific user.

- **user_id**: The UUID of the user whose profile to retrieve

This is a convenience endpoint to get a user's profile without knowing the profile ID.
            """,
            response_description="The user's profile information",
            responses={
                404: {"description": "Profile not found"}
            })
def read_user_profile(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_profile = service.ProfileService.get_profile_by_user(db, user_id=user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@router.put("/profiles/{profile_id}", 
            response_model=schemas.ProfileResponse,
            summary="Update profile",
            description="""
Update an existing user profile.

- **profile_id**: The UUID of the profile to update
- Only provided fields will be updated (partial updates supported)
            """,
            response_description="The updated profile information",
            responses={
                404: {"description": "Profile not found"}
            })
def update_profile(profile_id: uuid.UUID, profile_update: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    db_profile = service.ProfileService.update_profile(db, profile_id=profile_id, profile_update=profile_update)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@router.delete("/profiles/{profile_id}",
               status_code=status.HTTP_200_OK,
               summary="Delete profile",
               description="""
Delete a user profile.

- **profile_id**: The UUID of the profile to delete

Note: This only deletes the profile, not the user account.
               """,
               response_description="Confirmation message",
               responses={
                   404: {"description": "Profile not found"}
               })
def delete_profile(profile_id: uuid.UUID, db: Session = Depends(get_db)):
    success = service.ProfileService.delete_profile(db, profile_id=profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}
