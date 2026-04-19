from fastapi import HTTPException, status
from pydantic import ValidationError

from models.prescription_items import PrescriptionItems
from models.prescriptions import Prescriptions
from repositories.patients import PatientsRepository
from repositories.prescriptions import PrescriptionsRepository
from schemas.prescriptions import PrescriptionCreate, PrescriptionUpdate


class PrescriptionsService:
    def __init__(
        self,
        patients_repo: PatientsRepository,
        prescription_repo: PrescriptionsRepository,
    ):
        self.patients_repo = patients_repo
        self.prescription_repo = prescription_repo

    def create_prescription(self, data: dict) -> Prescriptions:
        try:
            validated = PrescriptionCreate(**data)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error.errors()
            )

        if not self.patients_repo.get_by_id(validated.patient_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
            )

        try:
            return self.prescription_repo.create(
                Prescriptions(
                    patient_id=validated.patient_id,
                    prescribed_by_id=validated.prescribed_by_id,
                    items=[
                        PrescriptionItems(**validated.prescription_item.model_dump())
                    ],
                )
            )
        except Exception as error:
            print(error)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create prescription",
            )

    def get_pending(self) -> list[Prescriptions]:
        return self.prescription_repo.get_all_pending()

    def update_status(self, prescription_id: str, data: dict) -> Prescriptions:
        try:
            validated = PrescriptionUpdate(**data)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error.errors()
            )

        prescription = self.prescription_repo.get_by_id(prescription_id)
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found"
            )

        for field, value in validated.model_dump(exclude_unset=True).items():
            setattr(prescription, field, value)

        return self.prescription_repo.update(prescription)

    def get_by_patient_id(self, patient_id: str):
        return self.prescription_repo.get_by_patient_id(patient_id)

    def get_by_patient_ids(self, patient_ids: list[str]):
        return self.prescription_repo.get_by_patient_ids(patient_ids)
