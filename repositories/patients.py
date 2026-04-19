from sqlmodel import Session, select
from typing import Any, Optional
from models.patients import Patients
from sqlalchemy import func

from schemas.patients import PatientsFilterField

TRGM_THRESHOLD = 0.3
TRGM_FIELDS = {PatientsFilterField.patientName, PatientsFilterField.gender}


class PatientsRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, patient: Patients):
        self.session.add(patient)
        self.session.commit()
        self.session.refresh(patient)

        return patient

    def stage(self, patient: Patients) -> Patients:
        self.session.add(patient)
        self.session.flush()

        return patient

    def get_by_id(self, patient_id: str) -> Optional[Patients]:
        return self.session.get(Patients, patient_id)

    def get_all_by(
        self, field: PatientsFilterField, value: Any, limit: int = 20, offset: int = 0
    ):
        col = getattr(Patients, field.value)

        if field in TRGM_FIELDS:
            statement = (
                select(Patients)
                .where(func.similarity(col, value) > TRGM_THRESHOLD)
                .order_by(func.similarity(col, value).desc())
                .offset(offset)
                .limit(limit)
            )
        else:
            statement = select(Patients).where(col == value).offset(offset).limit(limit)

        return self.session.exec(statement)

    def count_records_by(self, field: PatientsFilterField, value: Any) -> int:
        col = getattr(Patients, field.value)
        condition = (
            func.similarity(col, value) > TRGM_THRESHOLD
            if field in TRGM_FIELDS
            else col == value
        )
        statement = select(func.count()).select_from(Patients).where(condition)

        return self.session.exec(statement).one()

    def get_all(self) -> list[Patients]:
        return list(self.session.exec(select(Patients)).all())

    def update(self, patient: Patients) -> Patients:
        self.session.add(patient)
        self.session.commit()
        self.session.refresh(patient)

        return patient

    def delete(self, patient: Patients) -> None:
        self.session.delete(patient)
        self.session.commit()
