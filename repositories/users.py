from sqlmodel import Session

from models.users import Users
from typing import Optional


class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: Users) -> Users:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def is_email_in_use(self, email: str) -> bool:
        return bool(self.session.get(Users, email))

    def get_by_id(self, user_id: str) -> Optional[Users]:
        return self.session.get(Users, user_id)

    def update(self, user: Users) -> Users:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
