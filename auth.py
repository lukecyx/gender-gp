from typing import Any, Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import PasswordHelper
from sqlmodel import Session, select

from config import settings
from db.session import get_session
from models.users import Users


password_helper = PasswordHelper()


class UserDatabase(BaseUserDatabase[Users, str]):
    """All of this code is just from the fastapi_users docs.

    It's sole purpose is just to get jwts for protected routes.

    In the real world, the JWT would already have been passed down and
    then validated with middleware.
    """

    def __init__(self, session: Session):
        self.session = session

    async def get(self, id: str) -> Optional[Users]:
        return self.session.get(Users, id)

    async def get_by_email(self, email: str) -> Optional[Users]:
        return self.session.exec(select(Users).where(Users.email == email)).first()

    async def create(self, create_dict: dict[str, Any]) -> Users:
        user = Users(**create_dict)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def update(self, user: Users, update_dict: dict[str, Any]) -> Users:
        for key, value in update_dict.items():
            setattr(user, key, value)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def delete(self, user: Users) -> None:
        self.session.delete(user)
        self.session.commit()


class UserManager(BaseUserManager[Users, str]):
    reset_password_token_secret = settings.secret_key
    verification_token_secret = settings.secret_key

    def parse_id(self, value: Any) -> str:
        return str(value)

    async def on_after_register(self, user: Users, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_db(session: Session = Depends(get_session)):
    yield UserDatabase(session)


async def get_user_manager(user_db: UserDatabase = Depends(get_user_db)):
    yield UserManager(user_db, password_helper)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret_key,
        lifetime_seconds=settings.access_token_expire_minutes * 60,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[Users, str](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
