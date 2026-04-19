from fastapi import APIRouter, Depends, status
from typing import Optional

from dependencies import current_active_user, get_patients_service
from utils.pagination import Page, PaginationParams
from schemas.patients import (
    PatientsCreate,
    PatientsCreateResponse,
    PatientsUpdate,
    PatientstOut,
    PatientsFilterField,
)
from services.patients import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/", dependencies=[Depends(current_active_user)])
async def get_patient():
    return {"Patient": "Zero"}


@router.get(
    "/all",
    response_model=Page[PatientstOut],
    dependencies=[Depends(current_active_user)],
)
async def fetch_all_patients_by(
    pagination: PaginationParams = Depends(),
    service: PatientService = Depends(get_patients_service),
    field: Optional[PatientsFilterField] = None,
    value: Optional[str] = None,
):
    return service.get_all_patients_by(field, value, pagination)


@router.post(
    "/create",
    response_model=PatientsCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_patient(
    body: PatientsCreate, service: PatientService = Depends(get_patients_service)
):
    """This is the only public route.


    Presumably a user signing up, wants to become a patient so should be public.
    """
    return service.create_patient(body.model_dump())


@router.put(
    "/update/{patient_id}",
    response_model=PatientsCreateResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(current_active_user)],
)
async def update_patient(
    patient_id: str,
    body: PatientsUpdate,
    service: PatientService = Depends(get_patients_service),
):
    return service.update_patient(body.model_dump(exclude_unset=True), patient_id)
