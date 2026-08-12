from datetime import datetime, timedelta, timezone
from uuid import uuid4
import pytest

from app.pki import assert_certificate_usable, issue_certificate_record


def test_certificate_is_valid_inside_window() -> None:
    country = uuid4()
    record = issue_certificate_record("vehicle:V-001", country, "SERIAL-001", datetime.now(timezone.utc) + timedelta(days=30))
    assert record.valid_now
    assert_certificate_usable(record, country)


def test_certificate_country_isolation() -> None:
    record = issue_certificate_record("vehicle:V-001", uuid4(), "SERIAL-002", datetime.now(timezone.utc) + timedelta(days=30))
    with pytest.raises(PermissionError, match="country scope"):
        assert_certificate_usable(record, uuid4())


def test_expired_certificate_cannot_be_issued() -> None:
    with pytest.raises(ValueError):
        issue_certificate_record("vehicle:V-001", uuid4(), "SERIAL-003", datetime.now(timezone.utc) - timedelta(seconds=1))
