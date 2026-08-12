import pytest
from app.mfa import create_mfa_setup, verify_totp


def test_mfa_totp_roundtrip():
    setup = create_mfa_setup("user@example.com")
    assert setup.secret
    assert setup.otpauth_uri.startswith("otpauth://totp/")
    assert len(setup.recovery_codes) == 10
