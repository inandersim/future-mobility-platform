from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CorridorStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    RESTRICTED = "restricted"
    CLOSED = "closed"


@dataclass(frozen=True)
class CorridorPoint:
    latitude: float
    longitude: float
    altitude_m: float


@dataclass(frozen=True)
class VirtualCorridor:
    id: str
    country_id: str
    name: str
    lower_altitude_m: float
    upper_altitude_m: float
    status: CorridorStatus = CorridorStatus.DRAFT
    points: tuple[CorridorPoint, ...] = ()

    def contains_altitude(self, altitude_m: float) -> bool:
        return self.lower_altitude_m <= altitude_m <= self.upper_altitude_m

    def contains_country(self, country_id: str) -> bool:
        return self.country_id == country_id


def validate_altitude_band(lower: float, upper: float) -> None:
    if lower < 0 or upper <= lower:
        raise ValueError("invalid corridor altitude band")
