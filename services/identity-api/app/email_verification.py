from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import secrets

TOKEN_BYTES = 32
TOKEN_TTL_MINUTES = 30


def generate_verification_token() -> tuple[str, str, datetime]:
    token = secrets.token_urlsafe(TOKEN_BYTES)
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL_MINUTES)
    return token, digest, expires_at


def hash_verification_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
