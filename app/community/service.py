from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas


class BoardService:
    @staticmethod
    def create_board(db: Session, board: schemas.BoardCreate) -> models.Board:
        db_board = models.Board(
            title=board.title,
            description=board.description
        )
        db.add(db_board)
        db.commit()
        db.refresh(db_board)
        return db_board

    @staticmethod
    def get_board(db: Session, board_id: int) -> Optional[models.Board]:
        return db.query(models.Board).filter(models.Board.id == board_id).first()

    @staticmethod
    def get_boards(db: Session, skip: int = 0, limit: int = 100) -> List[models.Board]:
        return db.query(models.Board).offset(skip).limit(limit).all()

    @staticmethod
    def update_board(db: Session, board_id: int, board_update: schemas.BoardUpdate) -> Optional[models.Board]:
        db_board = db.query(models.Board).filter(models.Board.id == board_id).first()
        if db_board:
            update_data = board_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_board, field, value)
            db.commit()
            db.refresh(db_board)
        return db_board

    @staticmethod
    def delete_board(db: Session, board_id: int) -> bool:
        db_board = db.query(models.Board).filter(models.Board.id == board_id).first()
        if db_board:
            db.delete(db_board)
            db.commit()
            return True
        return False


class PostService:
    @staticmethod
    def create_post(db: Session, post: schemas.PostCreate, author_id: int) -> models.Post:
        db_post = models.Post(
            board_id=post.board_id,
            author_id=author_id,
            title=post.title,
            contents=post.contents
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    @staticmethod
    def get_post(db: Session, post_id: int) -> Optional[models.Post]:
        return db.query(models.Post).filter(models.Post.id == post_id).first()

    @staticmethod
    def get_posts_by_board(db: Session, board_id: int, skip: int = 0, limit: int = 100) -> List[models.Post]:
        return db.query(models.Post).filter(
            models.Post.board_id == board_id
        ).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate) -> Optional[models.Post]:
        db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if db_post:
            update_data = post_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_post, field, value)
            db.commit()
            db.refresh(db_post)
        return db_post

    @staticmethod
    def increment_view_count(db: Session, post_id: int) -> Optional[models.Post]:
        db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if db_post:
            db_post.view_count += 1
            db.commit()
            db.refresh(db_post)
        return db_post

    @staticmethod
    def increment_like_count(db: Session, post_id: int) -> Optional[models.Post]:
        db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if db_post:
            db_post.like_count += 1
            db.commit()
            db.refresh(db_post)
        return db_post

    @staticmethod
    def decrement_like_count(db: Session, post_id: int) -> Optional[models.Post]:
        db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if db_post and db_post.like_count > 0:
            db_post.like_count -= 1
            db.commit()
            db.refresh(db_post)
        return db_post


class CommentService:
    @staticmethod
    def create_comment(db: Session, comment: schemas.CommentCreate, author_id: int) -> models.Comment:
        db_comment = models.Comment(
            post_id=comment.post_id,
            author_id=author_id,
            contents=comment.contents,
            parent_id=comment.parent_id
        )
        db.add(db_comment)
        
        # Update comment count on post
        db_post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
        if db_post:
            db_post.comment_count += 1
        
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @staticmethod
    def get_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
        return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

    @staticmethod
    def get_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[models.Comment]:
        return db.query(models.Comment).filter(
            models.Comment.post_id == post_id
        ).order_by(models.Comment.created_at.asc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentUpdate) -> Optional[models.Comment]:
        db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
        if db_comment:
            update_data = comment_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_comment, field, value)
            db.commit()
            db.refresh(db_comment)
        return db_comment


class PostTagService:
    @staticmethod
    def add_tag(db: Session, post_id: int, tag: str) -> models.PostTag:
        db_tag = models.PostTag(post_id=post_id, tag=tag)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag

    @staticmethod
    def get_tags_by_post(db: Session, post_id: int) -> List[models.PostTag]:
        return db.query(models.PostTag).filter(models.PostTag.post_id == post_id).all()

    @staticmethod
    def remove_tag(db: Session, post_id: int, tag: str) -> bool:
        db_tag = db.query(models.PostTag).filter(
            models.PostTag.post_id == post_id,
            models.PostTag.tag == tag
        ).first()
        if db_tag:
            db.delete(db_tag)
            db.commit()
            return True
        return False
