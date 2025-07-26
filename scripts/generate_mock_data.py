from faker import Faker
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(project_root)
sys.path.append(project_root)

from config.config import settings
from app.user.models import User, Profile
from app.church.models import Church

fake = Faker()

engine = create_engine(settings.DATABASE_URL, echo=True)  # echo=True for debugging

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def generate_mock_user() -> dict:
    return {
        "created_at": fake.date_time_this_year(),
        "is_blocked": fake.boolean(),
        "is_admin": fake.boolean(),
    }

def generate_mock_profile(user_id: int, church_id: int) -> dict:
    return {
        "user_id": user_id,
        "created_at": fake.date_time(),
        "nickname": fake.name(),
        "thumbnail": fake.image_url(),
        "church_id": church_id,
    }

def generate_mock_church() -> dict:
    return {
        "name": fake.company(),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
    }

def seed_mock_churches(db: Session, count: int = 5):
    for _ in range(count):
        church = generate_mock_church()
        db_church = Church(**church)
        db.add(db_church)
        db.flush()

def seed_mock_users(db: Session, count: int = 5):
    church = db.query(Church).first()
    for _ in range(count):
        user = generate_mock_user()
        db_user = User(**user)
        db.add(db_user)
        db.flush()
        profile = generate_mock_profile(db_user.id, church.id)
        db_profile = Profile(**profile)
        db.add(db_profile)
        db.flush()
        db.commit()

def main():
    db = SessionLocal()
    print(settings.DATABASE_URL)
    seed_mock_churches(db, 5)
    seed_mock_users(db, 5)

if __name__ == "__main__":
    main()