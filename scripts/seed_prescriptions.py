import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import models  # noqa: F401 — register models with SQLModel metadata
from datetime import datetime, timezone
from random import choice, randint

from sqlmodel import Session, select

from db.session import engine
from models.patients import Patients
from models.prescription_items import PrescriptionItems
from models.prescriptions import Prescriptions, PrescriptionStatus
from models.staff import Staff

MEDICATIONS = [
    {"medication_name": "Estradiol valerate", "dosage": "2mg", "frequency": "Once daily", "duration_days": "90"},
    {"medication_name": "Estradiol valerate", "dosage": "4mg", "frequency": "Once daily", "duration_days": "90"},
    {"medication_name": "Estradiol gel", "dosage": "1.5mg", "frequency": "Once daily", "duration_days": "90"},
    {"medication_name": "Spironolactone", "dosage": "50mg", "frequency": "Twice daily", "duration_days": "90"},
    {"medication_name": "Spironolactone", "dosage": "100mg", "frequency": "Once daily", "duration_days": "60"},
    {"medication_name": "Testosterone (Testogel)", "dosage": "50mg", "frequency": "Once daily", "duration_days": "60"},
    {"medication_name": "Testosterone (Testogel)", "dosage": "25mg", "frequency": "Once daily", "duration_days": "60"},
    {"medication_name": "Progesterone", "dosage": "100mg", "frequency": "Once nightly", "duration_days": "90"},
    {"medication_name": "Bicalutamide", "dosage": "25mg", "frequency": "Once daily", "duration_days": "90"},
    {"medication_name": "Finasteride", "dosage": "5mg", "frequency": "Once daily", "duration_days": "90"},
]

STATUSES = list(PrescriptionStatus)


def seed(prescriptions_per_patient: int = 3):
    with Session(engine) as session:
        patients = session.exec(select(Patients)).all()
        if not patients:
            print("No patients found — run seed_patients.py first.", file=sys.stderr)
            sys.exit(1)

        doctors = session.exec(select(Staff)).all()
        if not doctors:
            print("No staff found — run seed.py first.", file=sys.stderr)
            sys.exit(1)

        now = datetime.now(timezone.utc)
        count = 0

        for patient in patients:
            for _ in range(prescriptions_per_patient):
                doctor = choice(doctors)
                status = choice(STATUSES)
                dispensed_at = now if status == PrescriptionStatus.completed else None

                prescription = Prescriptions(
                    patient_id=patient.id,
                    issued_at=now,
                    status=status,
                    prescribed_by_id=doctor.id,
                    dispensed_at=dispensed_at,
                )
                session.add(prescription)
                session.flush()

                for item in [choice(MEDICATIONS) for _ in range(randint(1, 3))]:
                    session.add(PrescriptionItems(prescription_id=prescription.id, **item))

                count += 1

        session.commit()
        print(f"Seeded {count} prescriptions across {len(patients)} patients.")


if __name__ == "__main__":
    seed()
