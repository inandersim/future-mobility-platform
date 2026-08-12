from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class CertificateStatus(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


@dataclass(frozen=True)
class CertificateRecord:
    id: UUID
    subject: str
    country_id: UUID
    status: CertificateStatus
    serial_number: str
    not_before: datetime
    not_after: datetime

    @property
    def valid_now(self) -> bool:
        now = datetime.now(timezone.utc)
        return self.status == CertificateStatus.ACTIVE and self.not_before <= now <= self.not_after


def issue_certificate_record(subject: str, country_id: UUID, serial_number: str, not_after: datetime) -> CertificateRecord:
    now = datetime.now(timezone.utc)
    if not_after <= now:
        raise ValueError("certificate expiry must be in the future")
    return CertificateRecord(uuid4(), subject, country_id, CertificateStatus.ACTIVE, serial_number, now, not_after)


def assert_certificate_usable(record: CertificateRecord, request_country_id: UUID) -> None:
    if record.country_id != request_country_id:
        raise PermissionError("certificate country scope violation")
    if not record.valid_now:
        raise PermissionError("certificate is not valid")
