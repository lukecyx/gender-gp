from sqlalchemy.orm import selectinload
from sqlmodel import Session, col, select
from typing import List, Optional

from models.prescriptions import Prescriptions, PrescriptionStatus


class PrescriptionsRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, prescription: Prescriptions) -> Prescriptions:
        self.session.add(prescription)
        self.session.commit()
        self.session.refresh(prescription)

        return prescription

    def get_all_pending(self) -> List[Prescriptions]:
        return list(
            self.session.exec(
                select(Prescriptions).where(
                    Prescriptions.status == PrescriptionStatus.pending
                )
            ).all()
        )

    def get_by_id(self, prescription_id: str) -> Optional[Prescriptions]:
        return self.session.get(Prescriptions, prescription_id)

    def get_by_patient_ids(self, patient_ids: list[str]) -> list[Prescriptions]:
        return list(
            self.session.exec(
                select(Prescriptions)
                .where(col(Prescriptions.patient_id).in_(patient_ids))
                .options(selectinload(Prescriptions.items))  # type: ignore[arg-type]
            ).all()
        )

    def get_by_patient_id(self, patient_id: str) -> list[Prescriptions]:
        return list(
            self.session.exec(
                select(Prescriptions)
                .where(Prescriptions.patient_id == patient_id)
                .options(selectinload(Prescriptions.items))  # type: ignore[arg-type]
            ).all()
        )

    def update(self, prescription: Prescriptions) -> Prescriptions:
        self.session.add(prescription)
        self.session.commit()
        self.session.refresh(prescription)

        return prescription
