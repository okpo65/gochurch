from faker import Faker
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import sys
import random
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(project_root)
sys.path.append(project_root)

from config.config import settings
from app.user.models import User
from app.community.models import Board, Post, Comment, PostTag

fake = Faker()

engine = create_engine(settings.DATABASE_URL, echo=True)  # echo=True for debugging

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

post_titles = [
    '오늘의 말씀: 로마서 12장 2절',
    '함께 기도해주세요',
    '나는 왜 기도해도 응답이 없을까?',
    '매일 10분 말씀 챌린지 ✨',
    '오늘 하루 감사 제목 1가지!',

]

board_titles = [
    '묵상 나눔',
    '기도 요청 나눔방',
    '신앙 Q&A',
]

post_contents = [
    '너희는 이 세대를 본받지 말고 오직 마음을 새롭게 함으로 변화를 받아…',
    '샬롬! 최근 가족 중 한 분이 아프셔서 병원에 입원하셨어요. 마음이 무겁고 지쳐 있는 상황인데, 형제자매 여러분의 기도가 큰 힘이 될 것 같아요. 함께 중보해주실 수 있을까요? 💒',
    '"기도는 하는데, 왜 내 삶은 그대로일까?" 이런 생각 들어보신 적 있으신가요? 기도 응답에 대해, 기다림에 대해, 여러분이 경험한 이야기를 나눠주세요. 여러분의 삶이 누군가에겐 큰 위로가 될 거예요.',
    '이번 주는 요한복음을 함께 읽어요!📖 오늘의 분량: 요한복음 1장💡 미션: 한 구절 필사 + 느낀 점 댓글로 나누기함께 말씀에 젖어가는 기쁨, 같이 누려요! 🙏',
    '요즘 작은 것에도 감사하기가 쉽지 않죠.그래서 오늘 하루를 돌아보며 "감사한 일 1가지"만 댓글로 나눠보아요.🍞 저는 아침에 먹은 따뜻한 빵 한 조각이 참 감사했어요. 여러분은요?',
]

comment_contents = [
    '오늘 하루 감사한 일 1가지를 댓글로 나눠보아요!',
    '댓글 댓글!',
    '댓글 댓글123123!',
    '댓글 댓글!',
    '좋아요 드립니다!'
]

tag_contents = [
    '기도',
    '묵상',
    '영적 성장',
    '소소한 일상 속 감사',
]


def generate_mock_post(board_id: int, author_id: int) -> dict:
    return {
        "board_id": board_id,
        "author_id": author_id,
        "title": post_titles[random.randint(0, len(post_titles) - 1)],
        "contents": post_contents[random.randint(0, len(post_contents) - 1)],
        "created_at": fake.date_time(),
        "updated_at": fake.date_time(),
        "like_count": fake.random_int(min=0, max=100),
        "comment_count": fake.random_int(min=0, max=10),
        "view_count": fake.random_int(min=0, max=100),
    }

def generate_mock_board() -> dict:
    return {
        "title": board_titles[random.randint(0, len(board_titles) - 1)],
        "description": "",
        "created_at": fake.date_time(),
    }

def generate_mock_comment(post_id: int, author_id: int) -> dict:
    return {
        "post_id": post_id,
        "author_id": author_id,
        "contents": comment_contents[random.randint(0, len(comment_contents) - 1)],
        "created_at": fake.date_time(),
    }

def main():
    db = SessionLocal()
    print(settings.DATABASE_URL)
    for i in range(5):
        board = generate_mock_board()
        db_board = Board(**board)
        db.add(db_board)
        db.flush()

    for post_title, post_content in zip(post_titles, post_contents):
        board_sample_id = random.choice(db.query(Board).all()).id
        author_sample_id = random.choice(db.query(User).all()).id
        post = generate_mock_post(board_sample_id, author_sample_id)
        db_post = Post(**post)
        db.add(db_post)
        db.flush()

    for comment_content in comment_contents:
        post_sample_id = random.choice(db.query(Post).all()).id
        author_sample_id = random.choice(db.query(User).all()).id
        comment = generate_mock_comment(post_sample_id, author_sample_id)
        db_comment = Comment(**comment)
        db.add(db_comment)
        db.flush()
    db.commit()

if __name__ == "__main__":
    main()