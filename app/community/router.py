from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from . import schemas, service


router = APIRouter(prefix="/boards", tags=["boards"])


# Board endpoints
@router.post("/", response_model=schemas.BoardResponse)
def create_board(board: schemas.BoardCreate, db: Session = Depends(get_db)):
    return service.BoardService.create_board(db=db, board=board)


@router.get("/", response_model=List[schemas.BoardResponse])
def read_boards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    boards = service.BoardService.get_boards(db, skip=skip, limit=limit)
    return boards


@router.get("/{board_id}", response_model=schemas.BoardResponse)
def read_board(board_id: int, db: Session = Depends(get_db)):
    db_board = service.BoardService.get_board(db, board_id=board_id)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board


@router.put("/{board_id}", response_model=schemas.BoardResponse)
def update_board(board_id: int, board_update: schemas.BoardUpdate, db: Session = Depends(get_db)):
    db_board = service.BoardService.update_board(db, board_id=board_id, board_update=board_update)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board


@router.delete("/{board_id}")
def delete_board(board_id: int, db: Session = Depends(get_db)):
    success = service.BoardService.delete_board(db, board_id=board_id)
    if not success:
        raise HTTPException(status_code=404, detail="Board not found")
    return {"message": "Board deleted successfully"}


# Post endpoints
@router.post("/{board_id}/posts", response_model=schemas.PostResponse)
def create_post(board_id: int, post: schemas.PostCreate, author_id: int, db: Session = Depends(get_db)):
    post.board_id = board_id
    return service.PostService.create_post(db=db, post=post, author_id=author_id)


@router.get("/{board_id}/posts", response_model=List[schemas.PostResponse])
def read_posts(board_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = service.PostService.get_posts_by_board(db, board_id=board_id, skip=skip, limit=limit)
    return posts


@router.get("/posts/{post_id}", response_model=schemas.PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    # Increment view count
    service.PostService.increment_view_count(db, post_id=post_id)
    
    db_post = service.PostService.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db)):
    db_post = service.PostService.update_post(db, post_id=post_id, post_update=post_update)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


# Comment endpoints
@router.post("/posts/{post_id}/comments", response_model=schemas.CommentResponse)
def create_comment(post_id: int, comment: schemas.CommentCreate, author_id: int, db: Session = Depends(get_db)):
    comment.post_id = post_id
    return service.CommentService.create_comment(db=db, comment=comment, author_id=author_id)


@router.get("/posts/{post_id}/comments", response_model=List[schemas.CommentResponse])
def read_comments(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = service.CommentService.get_comments_by_post(db, post_id=post_id, skip=skip, limit=limit)
    return comments


@router.get("/comments/{comment_id}", response_model=schemas.CommentResponse)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = service.CommentService.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.put("/comments/{comment_id}", response_model=schemas.CommentResponse)
def update_comment(comment_id: int, comment_update: schemas.CommentUpdate, db: Session = Depends(get_db)):
    db_comment = service.CommentService.update_comment(db, comment_id=comment_id, comment_update=comment_update)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


# Post tag endpoints
@router.post("/posts/{post_id}/tags", response_model=schemas.PostTagResponse)
def add_post_tag(post_id: int, tag: str, db: Session = Depends(get_db)):
    return service.PostTagService.add_tag(db=db, post_id=post_id, tag=tag)


@router.get("/posts/{post_id}/tags", response_model=List[schemas.PostTagResponse])
def get_post_tags(post_id: int, db: Session = Depends(get_db)):
    tags = service.PostTagService.get_tags_by_post(db, post_id=post_id)
    return tags


@router.delete("/posts/{post_id}/tags/{tag}")
def remove_post_tag(post_id: int, tag: str, db: Session = Depends(get_db)):
    success = service.PostTagService.remove_tag(db, post_id=post_id, tag=tag)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag removed successfully"}
