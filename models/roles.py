from sqlmodel import Field, SQLModel
from uuid_extensions import uuid7


class Roles(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid7()), primary_key=True)
    name: str = Field(unique=True)
