from app.fleet import FleetStatus, VehicleOperationalStatus, can_assign_vehicle, can_start_mission


def test_only_available_vehicle_can_be_assigned() -> None:
    assert can_assign_vehicle(VehicleOperationalStatus.AVAILABLE)
    assert not can_assign_vehicle(VehicleOperationalStatus.MAINTENANCE)
    assert not can_assign_vehicle(VehicleOperationalStatus.GROUNDED)


def test_only_assigned_vehicle_can_start_mission() -> None:
    assert can_start_mission(VehicleOperationalStatus.ASSIGNED)
    assert not can_start_mission(VehicleOperationalStatus.AVAILABLE)
    assert not can_start_mission(VehicleOperationalStatus.IN_MISSION)


def test_fleet_defaults_to_active() -> None:
    assert FleetStatus.ACTIVE.value == "active"
