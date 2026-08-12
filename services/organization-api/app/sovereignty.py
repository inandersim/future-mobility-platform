from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


class SovereigntyViolation(PermissionError):
    pass


@dataclass(frozen=True)
class DataScope:
    country_id: UUID
    organization_id: UUID | None = None


def assert_country_scope(request_country: UUID, resource_country: UUID) -> None:
    if request_country != resource_country:
        raise SovereigntyViolation("Cross-country access is denied")


def assert_organization_scope(request_country: UUID, resource_country: UUID, request_org: UUID | None, resource_org: UUID | None) -> None:
    assert_country_scope(request_country, resource_country)
    if request_org is not None and resource_org is not None and request_org != resource_org:
        raise SovereigntyViolation("Cross-organization access is denied")
