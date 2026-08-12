from datetime import datetime, timedelta, timezone

import pytest

from app.security import create_access_token, create_refresh_token, decode_token, hash_password, hash_refresh_token, verify_password


def test_password_hash_round_trip() -> None:
    password = "A-strong-password-123!"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_access_token_claims() -> None:
    token = create_access_token("user-1", "session-1")
    claims = decode_token(token)
    assert claims["sub"] == "user-1"
    assert claims["sid"] == "session-1"
    assert claims["type"] == "access"


def test_refresh_token_claims() -> None:
    expires = datetime.now(timezone.utc) + timedelta(days=1)
    token = create_refresh_token("user-1", "session-1", expires)
    claims = decode_token(token)
    assert claims["sub"] == "user-1"
    assert claims["sid"] == "session-1"
    assert claims["type"] == "refresh"
    assert "jti" in claims


def test_refresh_hash_is_deterministic() -> None:
    token = "test-refresh-token"
    assert hash_refresh_token(token) == hash_refresh_token(token)
    assert hash_refresh_token(token) != hash_refresh_token("other-token")


def test_invalid_token_is_rejected() -> None:
    with pytest.raises(ValueError):
        decode_token("not-a-token")
