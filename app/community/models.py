from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.sql import func
from database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(Text, nullable=False)
    contents = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True))
    like_count = Column(Integer, nullable=False, default=0)
    comment_count = Column(Integer, nullable=False, default=0)
    view_count = Column(Integer, nullable=False, default=0)


class PostTag(Base):
    __tablename__ = "post_tags"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    tag = Column(Text, primary_key=True)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    contents = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
