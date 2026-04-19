from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from models.patients import Sex
from enum import Enum


class PatientBase(BaseModel):
    email: EmailStr
    name: str
    nhs_number: str
    dob: date
    sex: Sex
    gender: str
    age: int

    @field_validator("nhs_number")
    @classmethod
    def validate_nhs_number(cls, v: str) -> str:
        digits = v.replace(" ", "")

        if not digits.isdigit() or len(digits) != 10:
            raise ValueError("NHS number must be 10 digits")

        return digits

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Age must be greater than 0")

        return v


class PatientsCreate(PatientBase):
    password: str


class PatientsCreateResponse(BaseModel):
    id: str

    model_config = {"from_attributes": True}


class PatientsUpdate(BaseModel):
    name: Optional[str] = None
    nhs_number: Optional[str] = None
    dob: Optional[date] = None
    sex: Optional[Sex] = None
    gender: Optional[str] = None
    age: Optional[int] = None


class PatientstOut(BaseModel):
    id: str
    name: str
    # TODO: Who is allowed to see this?
    # nhs_number: str
    dob: date
    sex: Sex
    gender: str
    age: int


class PatientsFilterField(str, Enum):
    patientName = "name"
    age = "age"
    gender = "gender"
