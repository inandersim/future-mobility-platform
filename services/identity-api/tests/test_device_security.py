from app.device_security import create_device_challenge, create_device_fingerprint


def test_device_fingerprint_is_deterministic_and_non_reversible_format() -> None:
    first = create_device_fingerprint("windows|chrome|device-123")
    second = create_device_fingerprint("windows|chrome|device-123")
    assert first == second
    assert len(first) == 64
    assert "device-123" not in first


def test_device_challenge_is_random() -> None:
    assert create_device_challenge() != create_device_challenge()
