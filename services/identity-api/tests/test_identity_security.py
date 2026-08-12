from datetime import datetime, timedelta, timezone

from app.identity_security import is_locked, register_failed_login, reset_failed_logins


def test_lockout_after_threshold() -> None:
    attempts, locked_until = register_failed_login(4)
    assert attempts == 5
    assert locked_until is not None
    assert locked_until > datetime.now(timezone.utc)


def test_failed_login_below_threshold_does_not_lock() -> None:
    attempts, locked_until = register_failed_login(3)
    assert attempts == 4
    assert locked_until is None


def test_lock_state() -> None:
    assert is_locked(datetime.now(timezone.utc) + timedelta(minutes=1))
    assert not is_locked(datetime.now(timezone.utc) - timedelta(minutes=1))
    assert not is_locked(None)


def test_reset_failed_logins() -> None:
    assert reset_failed_logins() == (0, None)
