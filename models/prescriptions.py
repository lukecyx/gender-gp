from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Index
from uuid_extensions import uuid7

if TYPE_CHECKING:
    from models.medical_report import MedicalReport
    from models.patients import Patients
    from models.prescription_items import PrescriptionItems


class PrescriptionStatus(int, Enum):
    pending = 1
    completed = 2
    cancelled = 3


class Prescriptions(SQLModel, table=True):
    __table_args__ = (
        Index(
            "idx__prescription_status_issued_at", "status", "issued_at"
        ),  # Sort by recency
    )
    id: str = Field(default_factory=lambda: str(uuid7()), primary_key=True)
    patient_id: str = Field(foreign_key="patients.id", index=True)
    medical_report_id: Optional[str] = Field(
        default=None, foreign_key="medical_report.id", index=True, nullable=True
    )
    issued_at: Optional[datetime] = Field(default=None, nullable=True)
    dispensed_at: Optional[datetime] = Field(default=None, nullable=True)
    status: PrescriptionStatus = Field(default=PrescriptionStatus.pending, index=True)
    prescribed_by_id: str = Field(foreign_key="staff.id")  # Maybe needs an index
    dispensed_by_id: Optional[str] = Field(
        default=None, foreign_key="staff.id", nullable=True
    )

    patient: Optional["Patients"] = Relationship(back_populates="prescriptions")
    medical_report: Optional["MedicalReport"] = Relationship(
        back_populates="prescription"
    )
    items: List["PrescriptionItems"] = Relationship(back_populates="prescription")
