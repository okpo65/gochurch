from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class BoardBase(BaseModel):
    title: str = Field(description="Title of the discussion board", max_length=200)
    description: Optional[str] = Field(None, description="Description of the board's purpose")


class BoardCreate(BoardBase):
    class Config:
        schema_extra = {
            "example": {
                "title": "General Discussion",
                "description": "A place for general community discussions and announcements"
            }
        }


class BoardUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the discussion board", max_length=200)
    description: Optional[str] = Field(None, description="Description of the board's purpose")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Updated General Discussion",
                "description": "Updated description for the board"
            }
        }


class BoardResponse(BoardBase):
    id: uuid.UUID = Field(description="Unique identifier for the board")
    created_at: datetime = Field(description="When the board was created")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440003",
                "title": "General Discussion",
                "description": "A place for general community discussions and announcements",
                "created_at": "2024-01-15T10:00:00Z"
            }
        }


class PostBase(BaseModel):
    title: str = Field(description="Title of the post", max_length=200)
    contents: str = Field(description="Main content of the post")


class PostCreate(PostBase):
    board_id: uuid.UUID = Field(description="UUID of the board this post belongs to")
    
    class Config:
        schema_extra = {
            "example": {
                "board_id": "550e8400-e29b-41d4-a716-446655440003",
                "title": "Welcome to our community!",
                "contents": "Hello everyone! Welcome to our church community board. Feel free to introduce yourselves and share what's on your heart."
            }
        }


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the post", max_length=200)
    contents: Optional[str] = Field(None, description="Main content of the post")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Updated: Welcome to our community!",
                "contents": "Updated content with more information..."
            }
        }


class PostResponse(PostBase):
    id: uuid.UUID = Field(description="Unique identifier for the post")
    board_id: uuid.UUID = Field(description="UUID of the board this post belongs to")
    author_id: uuid.UUID = Field(description="UUID of the user who created this post")
    created_at: datetime = Field(description="When the post was created")
    updated_at: Optional[datetime] = Field(None, description="When the post was last updated")
    like_count: int = Field(description="Number of likes this post has received")
    comment_count: int = Field(description="Number of comments on this post")
    view_count: int = Field(description="Number of times this post has been viewed")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440004",
                "board_id": "550e8400-e29b-41d4-a716-446655440003",
                "author_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Welcome to our community!",
                "contents": "Hello everyone! Welcome to our church community board.",
                "created_at": "2024-01-15T11:00:00Z",
                "updated_at": None,
                "like_count": 5,
                "comment_count": 3,
                "view_count": 25
            }
        }


class PostTagBase(BaseModel):
    tag: str = Field(description="Tag name", max_length=50)


class PostTagCreate(PostTagBase):
    post_id: uuid.UUID = Field(description="UUID of the post this tag belongs to")
    
    class Config:
        schema_extra = {
            "example": {
                "post_id": "550e8400-e29b-41d4-a716-446655440004",
                "tag": "welcome"
            }
        }


class PostTagResponse(PostTagBase):
    post_id: uuid.UUID = Field(description="UUID of the post this tag belongs to")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "post_id": "550e8400-e29b-41d4-a716-446655440004",
                "tag": "welcome"
            }
        }


class CommentBase(BaseModel):
    contents: str = Field(description="Content of the comment")


class CommentCreate(CommentBase):
    post_id: uuid.UUID = Field(description="UUID of the post this comment belongs to")
    parent_id: Optional[uuid.UUID] = Field(None, description="UUID of the parent comment (for nested comments)")
    
    class Config:
        schema_extra = {
            "example": {
                "post_id": "550e8400-e29b-41d4-a716-446655440004",
                "contents": "Thank you for the warm welcome! Excited to be part of this community.",
                "parent_id": None
            }
        }


class CommentUpdate(BaseModel):
    contents: Optional[str] = Field(None, description="Content of the comment")
    
    class Config:
        schema_extra = {
            "example": {
                "contents": "Updated comment content..."
            }
        }


class CommentResponse(CommentBase):
    id: uuid.UUID = Field(description="Unique identifier for the comment")
    post_id: uuid.UUID = Field(description="UUID of the post this comment belongs to")
    author_id: uuid.UUID = Field(description="UUID of the user who created this comment")
    parent_id: Optional[uuid.UUID] = Field(None, description="UUID of the parent comment (for nested comments)")
    created_at: datetime = Field(description="When the comment was created")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440005",
                "post_id": "550e8400-e29b-41d4-a716-446655440004",
                "author_id": "550e8400-e29b-41d4-a716-446655440000",
                "parent_id": None,
                "contents": "Thank you for the warm welcome! Excited to be part of this community.",
                "created_at": "2024-01-15T11:30:00Z"
            }
        }
