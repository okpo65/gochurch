from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from . import schemas, service

router = APIRouter(prefix="/churches", tags=["churches"])


@router.post("/", 
             response_model=schemas.ChurchResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new church",
             description="""
Create a new church in the directory.

- **name**: The name of the church (required)
- **address**: Physical address of the church (optional)
- **phone_number**: Contact phone number (optional)

Churches are used to organize users and can be referenced in user profiles and identity verifications.
             """,
             response_description="The created church information")
def create_church(church: schemas.ChurchCreate, db: Session = Depends(get_db)):
    return service.ChurchService.create_church(db=db, church=church)


@router.get("/", 
            response_model=List[schemas.ChurchResponse],
            summary="List all churches",
            description="""
Retrieve a paginated list of all churches in the directory.

- **skip**: Number of churches to skip (for pagination)
- **limit**: Maximum number of churches to return (max 100)

This endpoint is useful for populating church selection dropdowns in user interfaces.
            """,
            response_description="List of churches")
def read_churches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    churches = service.ChurchService.get_churches(db, skip=skip, limit=limit)
    return churches


@router.get("/{church_id}", 
            response_model=schemas.ChurchResponse,
            summary="Get church by ID",
            description="""
Retrieve a specific church by its ID.

- **church_id**: The ID of the church to retrieve

Example ID: `1`
            """,
            response_description="The requested church information",
            responses={
                404: {"description": "Church not found"}
            })
def read_church(church_id: int, db: Session = Depends(get_db)):
    db_church = service.ChurchService.get_church(db, church_id=church_id)
    if db_church is None:
        raise HTTPException(status_code=404, detail="Church not found")
    return db_church


@router.put("/{church_id}", 
            response_model=schemas.ChurchResponse,
            summary="Update church information",
            description="""
Update an existing church's information.

- **church_id**: The ID of the church to update
- Only provided fields will be updated (partial updates supported)

This is typically used by church administrators to keep contact information current.
            """,
            response_description="The updated church information",
            responses={
                404: {"description": "Church not found"}
            })
def update_church(church_id: int, church_update: schemas.ChurchUpdate, db: Session = Depends(get_db)):
    db_church = service.ChurchService.update_church(db, church_id=church_id, church_update=church_update)
    if db_church is None:
        raise HTTPException(status_code=404, detail="Church not found")
    return db_church


@router.delete("/{church_id}",
               status_code=status.HTTP_200_OK,
               summary="Delete church",
               description="""
Delete a church from the directory.

⚠️ **Warning**: This will affect all users and profiles associated with this church. 
Consider updating associated records before deletion.

- **church_id**: The ID of the church to delete
               """,
               response_description="Confirmation message",
               responses={
                   404: {"description": "Church not found"}
               })
def delete_church(church_id: int, db: Session = Depends(get_db)):
    success = service.ChurchService.delete_church(db, church_id=church_id)
    if not success:
        raise HTTPException(status_code=404, detail="Church not found")
    return {"message": "Church deleted successfully"}
