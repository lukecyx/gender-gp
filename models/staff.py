from sqlmodel import Field, SQLModel
from uuid_extensions import uuid7


class Staff(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid7()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", unique=True, index=True)
    employee_id: str = Field(unique=True)
    job_title: str
