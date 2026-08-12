from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AirspaceStatus(StrEnum):
    OPEN = "open"
    RESTRICTED = "restricted"
    PROHIBITED = "prohibited"
    TEMPORARY = "temporary"


@dataclass(frozen=True)
class AirspaceVolume:
    id: str
    country_id: str
    name: str
    lower_altitude_m: float
    upper_altitude_m: float
    status: AirspaceStatus

    def permits(self, country_id: str, altitude_m: float) -> bool:
        return (
            self.country_id == country_id
            and self.lower_altitude_m <= altitude_m <= self.upper_altitude_m
            and self.status == AirspaceStatus.OPEN
        )
