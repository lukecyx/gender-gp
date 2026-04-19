from pydantic import BaseModel


class PrescriptionItemBase(BaseModel):
    medication_name: str
    dosage: str
    frequency: str
    duration_days: str


class PrescriptionItemCreate(PrescriptionItemBase):
    prescription_id: str


class PrescriptionItemOut(PrescriptionItemBase):
    id: str
    prescription_id: str

    model_config = {"from_attributes": True}
