from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from sqlalchemy import Column, Index, JSON
from uuid_extensions import uuid7

from .mixins import TimestampMixin

if TYPE_CHECKING:
    from models.patients import Patients
    from models.prescriptions import Prescriptions


class MedicalReport(TimestampMixin, table=True):
    __tablename__ = "medical_report"  # type: ignore[assignment]
    __table_args__ = (
        Index("idx__medical_report_created_at_patient_id", "created_at", "patient_id"),
    )

    id: str = Field(default_factory=lambda: str(uuid7()), primary_key=True)
    patient_id: str = Field(foreign_key="patients.id", index=True)
    created_by_id: Optional[str] = Field(
        default=None, foreign_key="staff.id", nullable=True, index=True
    )
    diagnosis: str
    notes: Optional[list[str]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )

    patient: Optional["Patients"] = Relationship(back_populates="medical_reports")
    prescription: Optional["Prescriptions"] = Relationship(
        back_populates="medical_report"
    )
