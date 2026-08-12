from __future__ import annotations

from datetime import datetime, timedelta, timezone

MAX_FAILED_ATTEMPTS = 5
LOCK_MINUTES = 15


def is_locked(locked_until: datetime | None) -> bool:
    return locked_until is not None and locked_until > datetime.now(timezone.utc)


def register_failed_login(failed_attempts: int) -> tuple[int, datetime | None]:
    attempts = failed_attempts + 1
    if attempts >= MAX_FAILED_ATTEMPTS:
        return attempts, datetime.now(timezone.utc) + timedelta(minutes=LOCK_MINUTES)
    return attempts, None


def reset_failed_logins() -> tuple[int, None]:
    return 0, None
