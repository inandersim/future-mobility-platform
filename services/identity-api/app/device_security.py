from __future__ import annotations

import hashlib
import secrets


def create_device_fingerprint(raw_components: str) -> str:
    """Create a non-reversible device identifier from normalized client data."""
    return hashlib.sha256(raw_components.strip().encode("utf-8")).hexdigest()


def create_device_challenge() -> str:
    return secrets.token_urlsafe(32)
