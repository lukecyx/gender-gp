from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, status

from dependencies import current_active_user, get_prescriptions_service
from models.users import Users
from schemas.prescriptions import (
    PrescriptionCreate,
    PrescriptionCreateOut,
    PrescriptionOut,
    PrescriptionUpdate,
)
from services.prescriptions import PrescriptionsService

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])

CurrentUser = Annotated[Users, Depends(current_active_user)]


@router.post("/", response_model=list[PrescriptionOut])
def get_prescriptions_for_patients(
    _: CurrentUser,
    patient_ids: List[str] = Body(...),
    service: PrescriptionsService = Depends(get_prescriptions_service),
):
    return service.get_by_patient_ids(patient_ids)


@router.post(
    "/create",
    response_model=PrescriptionCreateOut,
    status_code=status.HTTP_201_CREATED,
)
def create_new_prescription(
    _: CurrentUser,
    body: PrescriptionCreate,
    service: PrescriptionsService = Depends(get_prescriptions_service),
):
    return service.create_prescription(body.model_dump())


@router.put("/update")
def update_patient_prescription(_: CurrentUser):
    """Updates a prescription"""
    return {}


@router.put(
    "/status/{prescription_id}",
    response_model=PrescriptionOut,
    status_code=status.HTTP_200_OK,
)
def update_prescription_status(
    _: CurrentUser,
    prescription_id: str,
    body: PrescriptionUpdate,
    service: PrescriptionsService = Depends(get_prescriptions_service),
):
    return service.update_status(prescription_id, body.model_dump(exclude_unset=True))


@router.get("/pending", response_model=list[PrescriptionOut])
def get_all_pending_prescriptions(
    _: CurrentUser,
    service: PrescriptionsService = Depends(get_prescriptions_service),
):
    return service.get_pending()
