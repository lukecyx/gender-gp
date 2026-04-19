from datetime import date
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Index
from sqlmodel import Field, Relationship
from uuid_extensions import uuid7

from .mixins import TimestampMixin

if TYPE_CHECKING:
    from models.medical_report import MedicalReport
    from models.prescriptions import Prescriptions
    from models.users import Users


class Sex(str, Enum):
    male = "male"
    female = "female"


class Patients(TimestampMixin, table=True):
    __table_args__ = (
        Index(
            "idx_patients_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )

    id: str = Field(default_factory=lambda: str(uuid7()), primary_key=True)
    user_id: Optional[str] = Field(
        default=None, foreign_key="users.id", unique=True, index=True
    )
    nhs_number: str = Field(unique=True)
    dob: date
    sex: Sex
    name: str
    age: int
    gender: str

    user: Optional["Users"] = Relationship(back_populates="patient")
    prescriptions: List["Prescriptions"] = Relationship(back_populates="patient")
    medical_reports: List["MedicalReport"] = Relationship(back_populates="patient")
