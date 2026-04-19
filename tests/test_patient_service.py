from datetime import date

import pytest
from fastapi import HTTPException

from models.patients import Sex
from services.patients import PatientService
from utils.pagination import PaginationParams


VALID_CREATE_DATA = {
    "email": "alice@example.com",
    "password": "password123",
    "name": "Alice Smith",
    "nhs_number": "1234567890",
    "dob": date(1990, 1, 1),
    "sex": Sex.female,
    "gender": "female",
    "age": 34,
}


@pytest.fixture
def service(patients_repo, users_repo):
    return PatientService(patients_repo, users_repo)


class TestCreatePatient:
    def test_creates_patient(self, service, patients_repo, users_repo, mock_patient):
        users_repo.is_email_in_use.return_value = False
        patients_repo.create.return_value = mock_patient

        result = service.create_patient(VALID_CREATE_DATA)

        patients_repo.create.assert_called_once()

        assert result == mock_patient

    def test_raises_400_if_email_in_use(self, service, users_repo):
        users_repo.is_email_in_use.return_value = True

        with pytest.raises(HTTPException) as exc:
            service.create_patient(VALID_CREATE_DATA)

        assert exc.value.status_code == 400

    def test_raises_400_on_invalid_data(self, service, users_repo):
        users_repo.is_email_in_use.return_value = False

        with pytest.raises(HTTPException) as exc:
            service.create_patient({"email": "not-an-email"})

        assert exc.value.status_code == 400

    def test_raises_500_on_repo_failure(self, service, patients_repo, users_repo):
        users_repo.is_email_in_use.return_value = False
        patients_repo.create.side_effect = Exception("db error")

        with pytest.raises(HTTPException) as exc:
            service.create_patient(VALID_CREATE_DATA)

        assert exc.value.status_code == 500


class TestUpdatePatient:
    def test_updates_patient(self, service, patients_repo, mock_patient):
        patients_repo.get_by_id.return_value = mock_patient
        patients_repo.update.return_value = mock_patient

        result = service.update_patient({"name": "Bob Jones"}, "patient-1")

        assert result == mock_patient

        patients_repo.update.assert_called_once_with(mock_patient)

    def test_raises_404_if_not_found(self, service, patients_repo):
        patients_repo.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc:
            service.update_patient({"name": "Bob"}, "missing-id")

        assert exc.value.status_code == 404


class TestGetAllPatientsBy:
    def test_returns_paginated_results(self, service, patients_repo, mock_patient):
        patients_repo.count_records_by.return_value = 1
        patients_repo.get_all_by.return_value = [mock_patient]

        from schemas.patients import PatientsFilterField

        pagination = PaginationParams(page=1, page_size=20)
        result = service.get_all_patients_by(
            PatientsFilterField.patientName, "Alice", pagination
        )

        assert result.total == 1
        assert result.page == 1
        assert len(result.data) == 1
