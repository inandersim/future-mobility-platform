import pytest

from app.corridor import CorridorPoint, CorridorStatus, VirtualCorridor, validate_altitude_band


def test_corridor_altitude_band() -> None:
    corridor = VirtualCorridor(
        id="c1", country_id="tr", name="Istanbul-01",
        lower_altitude_m=120, upper_altitude_m=180,
        status=CorridorStatus.ACTIVE,
        points=(CorridorPoint(41.0, 29.0, 150),),
    )
    assert corridor.contains_altitude(150)
    assert not corridor.contains_altitude(200)
    assert corridor.contains_country("tr")
    assert not corridor.contains_country("de")


def test_invalid_altitude_band_is_rejected() -> None:
    with pytest.raises(ValueError):
        validate_altitude_band(200, 100)
