from datetime import date
from unittest.mock import MagicMock

import pytest

from models.patients import Patients, Sex
from models.prescriptions import Prescriptions, PrescriptionStatus
from models.prescription_items import PrescriptionItems


@pytest.fixture
def patients_repo():
    return MagicMock()


@pytest.fixture
def users_repo():
    return MagicMock()


@pytest.fixture
def prescription_repo():
    return MagicMock()


@pytest.fixture
def mock_patient():
    return Patients(
        id="patient-1",
        user_id="user-1",
        nhs_number="1234567890",
        name="Alice Smith",
        dob=date(1990, 1, 1),
        sex=Sex.female,
        gender="female",
        age=34,
    )


@pytest.fixture
def mock_prescription():
    return Prescriptions(
        id="rx-1",
        patient_id="patient-1",
        prescribed_by_id="staff-1",
        status=PrescriptionStatus.pending,
        items=[
            PrescriptionItems(
                prescription_id="rx-1",
                medication_name="Estradiol",
                dosage="2mg",
                frequency="daily",
                duration_days="90",
            )
        ],
    )
