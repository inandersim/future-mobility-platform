from datetime import datetime, timezone

from app.password_reset import generate_reset_token, hash_reset_token


def test_reset_token_is_random_and_hashable() -> None:
    token, digest, expires_at = generate_reset_token()
    assert len(token) > 40
    assert digest == hash_reset_token(token)
    assert expires_at > datetime.now(timezone.utc)


def test_reset_token_hash_does_not_equal_raw_token() -> None:
    token, digest, _ = generate_reset_token()
    assert digest != token
