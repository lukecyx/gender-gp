"""
Seed script for development. Run with: python seed.py
All passwords are SHA-256 hashes of "password" — NOT for production use.
"""

import hashlib
import sys
from datetime import date, datetime, timezone

from sqlmodel import Session, select

from db.session import engine
from models.contact_info import ContactInfo
from models.medical_report import MedicalReport
from models.patients import Patients, Sex
from models.prescription_items import PrescriptionItems
from models.prescriptions import Prescriptions, PrescriptionStatus
from models.roles import Roles
from models.staff import Staff
from models.user_roles import UserRoles
from models.users import Users

DEV_PASSWORD_HASH = hashlib.sha256(b"password").hexdigest()


def seed():
    with Session(engine) as session:
        # --- Roles ---
        role_names = ["admin", "doctor", "pharmacist", "receptionist"]
        roles: dict[str, Roles] = {}
        for name in role_names:
            existing = session.exec(select(Roles).where(Roles.name == name)).first()
            if existing:
                roles[name] = existing
            else:
                role = Roles(name=name)
                session.add(role)
                session.flush()
                roles[name] = role
                print(f"  Created role: {name}")

        # --- Staff users ---
        staff_data = [
            {
                "email": "dr.smith@clinic.dev",
                "username": "dr.smith",
                "employee_id": "EMP001",
                "job_title": "GP Doctor",
                "role": "doctor",
            },
            {
                "email": "j.patel@clinic.dev",
                "username": "j.patel",
                "employee_id": "EMP002",
                "job_title": "Pharmacist",
                "role": "pharmacist",
            },
            {
                "email": "admin@clinic.dev",
                "username": "admin",
                "employee_id": "EMP003",
                "job_title": "Practice Manager",
                "role": "admin",
            },
        ]

        staff_members: list[Staff] = []
        for s in staff_data:
            existing_user = session.exec(
                select(Users).where(Users.email == s["email"])
            ).first()
            if existing_user:
                staff_member = session.exec(
                    select(Staff).where(Staff.user_id == existing_user.id)
                ).first()
                if staff_member:
                    staff_members.append(staff_member)
                    continue

            user = Users(
                email=s["email"],
                username=s["username"],
                password_hash=DEV_PASSWORD_HASH,
            )
            session.add(user)
            session.flush()

            staff_member = Staff(
                user_id=user.id, employee_id=s["employee_id"], job_title=s["job_title"]
            )
            session.add(staff_member)
            session.flush()

            user_role = UserRoles(user_id=user.id, role_id=roles[s["role"]].id)
            session.add(user_role)

            staff_members.append(staff_member)
            print(f"  Created staff: {s['email']} ({s['job_title']})")

        doctor = staff_members[0]
        pharmacist = staff_members[1]

        # --- Patients ---
        patients_data = [
            {
                "email": "alice.jones@example.dev",
                "username": "alice.jones",
                "nhs_number": "9000000001",
                "dob": date(1990, 3, 15),
                "sex": Sex.female,
                "name": "Alice Jones",
                "age": 35,
                "gender": "Woman",
                "phone_1": "07700900001",
                "address_line_1": "12 Rose Lane",
                "address_line_2": "Hackney",
                "address_line_3": "London E8 1AA",
            },
            {
                "email": "bob.taylor@example.dev",
                "username": "bob.taylor",
                "nhs_number": "9000000002",
                "dob": date(1985, 7, 22),
                "sex": Sex.male,
                "name": "Bob Taylor",
                "age": 40,
                "gender": "Man",
                "phone_1": "07700900002",
                "address_line_1": "34 Oak Street",
                "address_line_2": "Islington",
                "address_line_3": "London N1 2BT",
            },
            {
                "email": "charlie.morgan@example.dev",
                "username": "charlie.morgan",
                "nhs_number": "9000000003",
                "dob": date(1978, 11, 5),
                "sex": Sex.male,
                "name": "Charlie Morgan",
                "age": 47,
                "gender": "Non-binary",
                "phone_1": "07700900003",
                "address_line_1": "7 Elm Close",
                "address_line_2": "Southwark",
                "address_line_3": "London SE1 5QR",
            },
        ]

        patients: list[Patients] = []
        for p in patients_data:
            existing_user = session.exec(
                select(Users).where(Users.email == p["email"])
            ).first()
            if existing_user:
                patient = session.exec(
                    select(Patients).where(Patients.user_id == existing_user.id)
                ).first()
                if patient:
                    patients.append(patient)
                    continue

            user = Users(
                email=p["email"],
                username=p["username"],
                password_hash=DEV_PASSWORD_HASH,
            )
            session.add(user)
            session.flush()

            contact = ContactInfo(
                phone_1=p["phone_1"],
                address_line_1=p["address_line_1"],
                address_line_2=p.get("address_line_2"),
                address_line_3=p.get("address_line_3"),
            )
            session.add(contact)
            session.flush()

            patient = Patients(
                user_id=user.id,
                nhs_number=p["nhs_number"],
                dob=p["dob"],
                sex=p["sex"],
                contact_info_id=contact.id,
                name=p["name"],
                age=p["age"],
                gender=p["gender"],
            )
            session.add(patient)
            session.flush()

            user_role = UserRoles(user_id=user.id, role_id=roles["receptionist"].id)
            session.add(user_role)

            patients.append(patient)
            print(f"  Created patient: {p['email']}")

        # --- Medical reports & prescriptions ---
        report_data = [
            {
                "patient": patients[0],
                "diagnosis": "Gender dysphoria — initiating HRT",
                "notes": ["Patient referred by psychiatrist", "Baseline bloods taken"],
                "items": [
                    {
                        "medication_name": "Estradiol valerate",
                        "dosage": "2mg",
                        "frequency": "Once daily",
                        "duration_days": "90",
                    },
                    {
                        "medication_name": "Spironolactone",
                        "dosage": "50mg",
                        "frequency": "Twice daily",
                        "duration_days": "90",
                    },
                ],
            },
            {
                "patient": patients[1],
                "diagnosis": "Gender dysphoria — HRT review",
                "notes": ["Blood levels within target range", "Continue current dose"],
                "items": [
                    {
                        "medication_name": "Testosterone (Testogel)",
                        "dosage": "50mg",
                        "frequency": "Once daily",
                        "duration_days": "60",
                    },
                ],
            },
            {
                "patient": patients[2],
                "diagnosis": "Gender dysphoria — dose adjustment",
                "notes": ["Estradiol levels low, increasing dose"],
                "items": [
                    {
                        "medication_name": "Estradiol valerate",
                        "dosage": "4mg",
                        "frequency": "Once daily",
                        "duration_days": "90",
                    },
                ],
            },
        ]

        now = datetime.now(timezone.utc)
        for rd in report_data:
            patient: Patients = rd["patient"]
            existing_report = session.exec(
                select(MedicalReport).where(MedicalReport.patient_id == str(patient.id))
            ).first()
            if existing_report:
                continue

            report = MedicalReport(
                patient_id=patient.id,
                created_by_id=doctor.id,
                diagnosis=rd["diagnosis"],
                notes=rd["notes"],
            )
            session.add(report)
            session.flush()

            prescription = Prescriptions(
                patient_id=patient.id,
                medical_report_id=report.id,
                issued_at=now,
                status=PrescriptionStatus.pending,
                prescribed_by_id=doctor.id,
            )
            session.add(prescription)
            session.flush()

            for item in rd["items"]:
                session.add(PrescriptionItems(prescription_id=prescription.id, **item))

            print(f"  Created report + prescription for patient: {patient.nhs_number}")

        session.commit()
        print("\nSeed complete.")


if __name__ == "__main__":
    print("Seeding database...")
    try:
        seed()
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
