import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import models  # noqa: F401 — register models with SQLModel metadata
from random import choice, randint

from sqlmodel import Session

from auth import password_helper
from db.session import engine
from models.staff import Staff
from models.users import Users

NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah",
    "Ivan", "Julia", "Kevin", "Laura", "Mike", "Nina", "Oscar", "Paula",
]

JOB_TITLES = [
    "GP",
    "Practice Nurse",
    "Pharmacist",
    "Receptionist",
    "Practice Manager",
]


def seed(n: int = 10):
    with Session(engine) as session:
        for i in range(n):
            name = f"{choice(NAMES)} {choice(NAMES)}"
            email = f"staff_{i}@seed.dev"
            employee_id = f"EMP{str(randint(1000, 9999))}"

            user = Users(email=email, hashed_password=password_helper.hash("password123"))
            session.add(user)
            session.flush()

            staff = Staff(
                user_id=user.id,
                employee_id=employee_id,
                job_title=choice(JOB_TITLES),
            )
            session.add(staff)

        session.commit()
        print(f"Seeded {n} staff members.")


if __name__ == "__main__":
    seed()
