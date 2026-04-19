import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import models  # noqa: F401 — register models with SQLModel metadata
from datetime import date
from random import choice, randint

from sqlmodel import Session

from auth import password_helper
from db.session import engine
from models.patients import Patients, Sex
from models.users import Users

NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah",
    "Ivan", "Julia", "Kevin", "Laura", "Mike", "Nina", "Oscar", "Paula",
    "Quinn", "Rachel", "Steve", "Tina", "Uma", "Victor", "Wendy", "Xander",
    "Yasmine", "Zach",
]

GENDERS = ["male", "female", "non-binary", "prefer not to say"]


def random_nhs() -> str:
    return str(randint(1_000_000_000, 9_999_999_999))


def random_dob() -> date:
    return date(randint(1940, 2005), randint(1, 12), randint(1, 28))


def seed(n: int = 100):
    with Session(engine) as session:
        for i in range(n):
            name = f"{choice(NAMES)} {choice(NAMES)}"
            email = f"patient_{i}@seed.dev"

            user = Users(email=email, hashed_password=password_helper.hash("password123"))
            session.add(user)
            session.flush()

            dob = random_dob()
            sex = choice(list(Sex))
            patient = Patients(
                user_id=user.id,
                nhs_number=random_nhs(),
                name=name,
                dob=dob,
                sex=sex,
                gender=choice(GENDERS),
                age=(date.today() - dob).days // 365,
            )
            session.add(patient)

        session.commit()
        print(f"Seeded {n} patients.")


if __name__ == "__main__":
    seed()
