from app.schemas import MFAChallengeRequest


def test_mfa_challenge_schema_accepts_six_digit_code() -> None:
    payload = MFAChallengeRequest(
        email="pilot@example.com",
        password="correct-horse-battery-staple",
        code="123456",
    )
    assert payload.code == "123456"


def test_mfa_challenge_schema_rejects_non_numeric_code() -> None:
    try:
        MFAChallengeRequest(
            email="pilot@example.com",
            password="correct-horse-battery-staple",
            code="abc123",
        )
    except Exception:
        return
    raise AssertionError("invalid MFA code should be rejected")
