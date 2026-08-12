from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import secrets

RESET_TOKEN_TTL_MINUTES = 30


def generate_reset_token() -> tuple[str, str, datetime]:
    token = secrets.token_urlsafe(48)
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_TTL_MINUTES)
    return token, digest, expires_at


def hash_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
