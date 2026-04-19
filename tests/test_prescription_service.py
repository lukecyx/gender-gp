import pytest
from fastapi import HTTPException

from models.prescriptions import PrescriptionStatus
from services.prescriptions import PrescriptionsService


VALID_CREATE_DATA = {
    "patient_id": "patient-1",
    "prescribed_by_id": "staff-1",
    "prescription_item": {
        "medication_name": "Estradiol",
        "dosage": "2mg",
        "frequency": "daily",
        "duration_days": "90",
    },
}


@pytest.fixture
def service(patients_repo, prescription_repo):
    return PrescriptionsService(patients_repo, prescription_repo)


class TestCreatePrescription:
    def test_creates_prescription(
        self, service, patients_repo, prescription_repo, mock_patient, mock_prescription
    ):
        patients_repo.get_by_id.return_value = mock_patient
        prescription_repo.create.return_value = mock_prescription

        result = service.create_prescription(VALID_CREATE_DATA)

        prescription_repo.create.assert_called_once()

        assert result == mock_prescription

    def test_raises_404_if_patient_not_found(self, service, patients_repo):
        patients_repo.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc:
            service.create_prescription(VALID_CREATE_DATA)

        assert exc.value.status_code == 404

    def test_raises_400_on_invalid_data(self, service):
        with pytest.raises(HTTPException) as exc:
            service.create_prescription({"patient_id": "p-1"})

        assert exc.value.status_code == 400

    def test_raises_500_on_repo_failure(
        self, service, patients_repo, prescription_repo, mock_patient
    ):
        patients_repo.get_by_id.return_value = mock_patient
        prescription_repo.create.side_effect = Exception("db error")

        with pytest.raises(HTTPException) as exc:
            service.create_prescription(VALID_CREATE_DATA)

        assert exc.value.status_code == 500


class TestGetPending:
    def test_returns_pending_prescriptions(
        self, service, prescription_repo, mock_prescription
    ):
        prescription_repo.get_all_pending.return_value = [mock_prescription]

        result = service.get_pending()

        assert len(result) == 1
        assert result[0].status == PrescriptionStatus.pending

    def test_returns_empty_list_when_none_pending(self, service, prescription_repo):
        prescription_repo.get_all_pending.return_value = []

        result = service.get_pending()

        assert result == []


class TestUpdateStatus:
    def test_updates_status(self, service, prescription_repo, mock_prescription):
        prescription_repo.get_by_id.return_value = mock_prescription
        prescription_repo.update.return_value = mock_prescription

        result = service.update_status("rx-1", {"status": PrescriptionStatus.completed})

        assert result == mock_prescription
        prescription_repo.update.assert_called_once_with(mock_prescription)

    def test_raises_404_if_not_found(self, service, prescription_repo):
        prescription_repo.get_by_id.return_value = None

        with pytest.raises(HTTPException) as error:
            service.update_status(
                "missing-id", {"status": PrescriptionStatus.completed}
            )

        assert error.value.status_code == 404

    def test_raises_400_on_invalid_status(
        self, service, prescription_repo, mock_prescription
    ):
        prescription_repo.get_by_id.return_value = mock_prescription

        with pytest.raises(HTTPException) as error:
            service.update_status("rx-1", {"status": 99})

        assert error.value.status_code == 400
