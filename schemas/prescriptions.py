from datetime import datetime
from pydantic import BaseModel, model_validator

from typing import List, Optional
from models.prescriptions import PrescriptionStatus
from schemas.prescriptionItem import PrescriptionItemBase, PrescriptionItemOut


class PrescriptionBase(BaseModel):
    issued_at: datetime
    status: PrescriptionStatus
    prescribed_by_id: str
    dispensed_by_id: str


class PrescriptionCreate(BaseModel):
    patient_id: str
    prescribed_by_id: str
    prescription_item: PrescriptionItemBase


class PrescriptionCreateOut(BaseModel):
    id: str

    model_config = {"from_attributes": True}


class PrescriptionOut(BaseModel):
    id: str
    patient_id: str
    medical_report_id: Optional[str]
    issued_at: Optional[datetime]
    dispensed_at: Optional[datetime]
    status: PrescriptionStatus
    prescribed_by_id: str
    dispensed_by_id: Optional[str]
    items: List[PrescriptionItemOut] = []

    model_config = {"from_attributes": True}


class PrescriptionUpdate(BaseModel):
    status: Optional[PrescriptionStatus] = None
    dispensed_by_id: Optional[str] = None
    dispensed_at: Optional[datetime] = None
