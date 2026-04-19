from typing import Any
from fastapi import HTTPException, status
from pydantic import ValidationError

from auth import password_helper
from models.patients import Patients
from models.users import Users
from repositories.patients import PatientsRepository
from repositories.users import UsersRepository
from utils.pagination import PaginationParams
from schemas.patients import (
    PatientsCreate,
    PatientsFilterField,
    PatientsUpdate,
    PatientstOut,
)
from typing import Optional
from utils.pagination import Page
import math


class PatientService:
    def __init__(
        self,
        patients_repo: PatientsRepository,
        users_repo: UsersRepository,
    ):
        self.patients_repo = patients_repo
        self.users_repo = users_repo

    def create_patient(self, data: dict) -> Patients:
        try:
            validated = PatientsCreate(**data)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error.errors()
            )

        if self.users_repo.is_email_in_use(validated.email):
            # Caller should handle user friendly name
            # Don't immediately tell that the email is in use if someone is hitting the api

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create patient",
            )

        try:
            return self.patients_repo.create(
                Patients(
                    nhs_number=validated.nhs_number,
                    dob=validated.dob,
                    sex=validated.sex,
                    name=validated.name,
                    age=validated.age,
                    gender=validated.gender,
                    user=Users(
                        email=validated.email,
                        hashed_password=password_helper.hash(validated.password),
                    ),
                )
            )
        except Exception as error:
            print(error)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )

    def update_patient(self, data: dict, patient_id: str) -> Patients:
        try:
            validated = PatientsUpdate(**data)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error.errors()
            )

        patient = self.patients_repo.get_by_id(patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
            )

        for field, value in validated.model_dump(
            exclude_unset=True, exclude={"id"}
        ).items():
            setattr(patient, field, value)

        return self.patients_repo.update(patient)

    def get_all_patients_by(
        self,
        field: Optional[PatientsFilterField],
        value: Optional[Any],
        pagination: PaginationParams,
    ) -> Page[PatientstOut]:
        if field is not None and value is not None:
            total = self.patients_repo.count_records_by(field, value)
            patients = list(
                self.patients_repo.get_all_by(
                    field, value, limit=pagination.page_size, offset=pagination.offset
                )
            )
        else:
            all_patients = self.patients_repo.get_all()
            total = len(all_patients)
            patients = all_patients[
                pagination.offset : pagination.offset + pagination.page_size
            ]

        return Page(
            data=[
                PatientstOut.model_validate(p, from_attributes=True) for p in patients
            ],
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
            total_pages=math.ceil(total / pagination.page_size),
        )
