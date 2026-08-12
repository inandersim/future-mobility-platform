from app.mfa import create_mfa_setup, verify_totp
import pyotp


def test_mfa_setup_generates_secret_and_recovery_codes() -> None:
    setup = create_mfa_setup("pilot@example.com")
    assert len(setup.secret) >= 16
    assert setup.otpauth_uri.startswith("otpauth://totp/")
    assert len(setup.recovery_codes) == 10
    assert len(set(setup.recovery_codes)) == 10


def test_totp_verification() -> None:
    setup = create_mfa_setup("pilot@example.com")
    code = pyotp.TOTP(setup.secret).now()
    assert verify_totp(setup.secret, code)
    assert not verify_totp(setup.secret, "000000")
