from uuid import uuid4
import pytest
from app.registry import VehicleRegistrationError, VehicleRegistrationRequest, assert_vehicle_country, validate_registration


def request(approved: bool = True) -> VehicleRegistrationRequest:
    return VehicleRegistrationRequest(uuid4(), uuid4(), uuid4(), "TR-UAV-001", "SN-001", approved)


def test_registration_requires_approved_model() -> None:
    with pytest.raises(VehicleRegistrationError, match="certification"):
        validate_registration(request(False))


def test_registration_requires_registration_number() -> None:
    r = request()
    r = VehicleRegistrationRequest(r.country_id, r.manufacturer_id, r.model_id, " ", r.serial_number, True)
    with pytest.raises(VehicleRegistrationError, match="registration"):
        validate_registration(r)


def test_vehicle_country_isolation() -> None:
    with pytest.raises(PermissionError, match="country scope"):
        assert_vehicle_country(uuid4(), uuid4())
