from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from uuid_extensions import uuid7

if TYPE_CHECKING:
    from models.patients import Patients


class Users(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid7()), primary_key=True)
    username: Optional[str] = Field(default=None, nullable=True)
    email: str = Field(unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)

    patient: Optional["Patients"] = Relationship(back_populates="user")
