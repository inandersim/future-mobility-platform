from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class FleetStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RETIRED = "retired"


class VehicleOperationalStatus(StrEnum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    IN_MISSION = "in_mission"
    MAINTENANCE = "maintenance"
    GROUNDED = "grounded"
    OFFLINE = "offline"


@dataclass(frozen=True)
class Fleet:
    id: str
    country_id: str
    organization_id: str
    name: str
    status: FleetStatus = FleetStatus.ACTIVE


@dataclass(frozen=True)
class FleetVehicle:
    fleet_id: str
    vehicle_id: str
    operational_status: VehicleOperationalStatus = VehicleOperationalStatus.AVAILABLE


def can_assign_vehicle(vehicle_status: VehicleOperationalStatus) -> bool:
    return vehicle_status == VehicleOperationalStatus.AVAILABLE


def can_start_mission(vehicle_status: VehicleOperationalStatus) -> bool:
    return vehicle_status == VehicleOperationalStatus.ASSIGNED
