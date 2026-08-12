from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import hypot


class TrafficStatus(StrEnum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    EMERGENCY = "emergency"


@dataclass(frozen=True)
class TrafficTrack:
    id: str
    country_id: str
    vehicle_id: str
    latitude: float
    longitude: float
    altitude_m: float
    speed_mps: float
    heading_deg: float
    status: TrafficStatus = TrafficStatus.ACTIVE


def same_country(a: TrafficTrack, b: TrafficTrack) -> bool:
    return a.country_id == b.country_id


def horizontal_distance(a: TrafficTrack, b: TrafficTrack) -> float:
    return hypot(a.latitude - b.latitude, a.longitude - b.longitude)


def vertical_distance(a: TrafficTrack, b: TrafficTrack) -> float:
    return abs(a.altitude_m - b.altitude_m)


def separation_breach(
    a: TrafficTrack,
    b: TrafficTrack,
    horizontal_threshold: float,
    vertical_threshold_m: float,
) -> bool:
    if not same_country(a, b):
        return False
    return (
        horizontal_distance(a, b) < horizontal_threshold
        and vertical_distance(a, b) < vertical_threshold_m
    )
