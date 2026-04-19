from fastapi import Depends
from sqlmodel import Session

from auth import current_active_user
from db.session import get_session
from repositories.patients import PatientsRepository
from repositories.prescriptions import PrescriptionsRepository
from repositories.users import UsersRepository
from services.patients import PatientService
from services.prescriptions import PrescriptionsService

__all__ = ["get_session", "current_active_user", "get_patients_service", "get_prescriptions_service"]


def get_patients_service(db: Session = Depends(get_session)) -> PatientService:
    return PatientService(PatientsRepository(db), UsersRepository(db))


def get_prescriptions_service(db: Session = Depends(get_session)) -> PrescriptionsService:
    return PrescriptionsService(PatientsRepository(db), PrescriptionsRepository(db))
