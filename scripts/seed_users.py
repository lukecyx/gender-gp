import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import models  # noqa: F401
from sqlmodel import Session, select

from auth import password_helper
from db.session import engine
from models.users import Users


def seed():
    with Session(engine) as session:
        email = "user@example.com"
        existing = session.exec(select(Users).where(Users.email == email)).first()
        if existing:
            print(f"User {email} already exists.")
            return

        user = Users(
            email=email,
            hashed_password=password_helper.hash("string"),
        )
        session.add(user)
        session.commit()
        print(f"Created user: {email}")


if __name__ == "__main__":
    seed()
