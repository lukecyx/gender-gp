from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from uuid_extensions import uuid7

from .mixins import TimestampMixin

if TYPE_CHECKING:
    from models.prescriptions import Prescriptions


class PrescriptionItems(TimestampMixin, table=True):
    id: str = Field(default_factory=lambda: str(uuid7()), primary_key=True)
    prescription_id: Optional[str] = Field(
        default=None, foreign_key="prescriptions.id", index=True
    )
    medication_name: str = Field(
        index=True
    )  # NOTE: Should really be tri grammed for fuzzy searching
    dosage: str
    frequency: str
    duration_days: str

    prescription: Optional["Prescriptions"] = Relationship(back_populates="items")
