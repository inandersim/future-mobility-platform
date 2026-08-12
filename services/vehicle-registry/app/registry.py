from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


class VehicleRegistrationError(ValueError):
    pass


@dataclass(frozen=True)
class VehicleRegistrationRequest:
    country_id: UUID
    manufacturer_id: UUID
    model_id: UUID
    registration_number: str
    serial_number: str
    model_certification_approved: bool


def validate_registration(request: VehicleRegistrationRequest) -> None:
    if not request.model_certification_approved:
        raise VehicleRegistrationError("vehicle model certification is not approved")
    if not request.registration_number.strip():
        raise VehicleRegistrationError("registration number is required")
    if not request.serial_number.strip():
        raise VehicleRegistrationError("serial number is required")


def assert_vehicle_country(request_country_id: UUID, vehicle_country_id: UUID) -> None:
    if request_country_id != vehicle_country_id:
        raise PermissionError("vehicle country scope violation")
