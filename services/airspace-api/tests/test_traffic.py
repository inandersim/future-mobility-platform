from app.traffic import TrafficTrack, separation_breach


def track(track_id: str, country: str, lat: float, lon: float, alt: float) -> TrafficTrack:
    return TrafficTrack(track_id, country, f"v-{track_id}", lat, lon, alt, 20.0, 90.0)


def test_same_country_tracks_can_trigger_separation_breach() -> None:
    a = track("a", "tr", 41.0000, 29.0000, 150)
    b = track("b", "tr", 41.0005, 29.0005, 152)
    assert separation_breach(a, b, horizontal_threshold=0.001, vertical_threshold_m=5)


def test_cross_country_tracks_are_not_compared_as_domestic_traffic() -> None:
    a = track("a", "tr", 41.0, 29.0, 150)
    b = track("b", "de", 41.0, 29.0, 150)
    assert not separation_breach(a, b, horizontal_threshold=0.001, vertical_threshold_m=5)


def test_safe_vertical_separation() -> None:
    a = track("a", "tr", 41.0, 29.0, 150)
    b = track("b", "tr", 41.0, 29.0, 200)
    assert not separation_breach(a, b, horizontal_threshold=0.001, vertical_threshold_m=5)
