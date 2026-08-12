from app.airspace import AirspaceStatus, AirspaceVolume


def test_open_airspace_allows_matching_country_and_altitude() -> None:
    volume = AirspaceVolume("a1", "tr", "A1", 100, 200, AirspaceStatus.OPEN)
    assert volume.permits("tr", 150)


def test_restricted_airspace_denies_operation() -> None:
    volume = AirspaceVolume("a1", "tr", "A1", 100, 200, AirspaceStatus.RESTRICTED)
    assert not volume.permits("tr", 150)


def test_airspace_is_country_scoped() -> None:
    volume = AirspaceVolume("a1", "tr", "A1", 100, 200, AirspaceStatus.OPEN)
    assert not volume.permits("de", 150)
