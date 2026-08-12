from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class MissionStatus(StrEnum):
    DRAFT = "draft"
    PLANNING = "planning"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ABORTED = "aborted"


_ALLOWED_TRANSITIONS: dict[MissionStatus, frozenset[MissionStatus]] = {
    MissionStatus.DRAFT: frozenset({MissionStatus.PLANNING, MissionStatus.CANCELLED}),
    MissionStatus.PLANNING: frozenset({MissionStatus.APPROVED, MissionStatus.CANCELLED}),
    MissionStatus.APPROVED: frozenset({MissionStatus.SCHEDULED, MissionStatus.CANCELLED}),
    MissionStatus.SCHEDULED: frozenset({MissionStatus.READY, MissionStatus.CANCELLED}),
    MissionStatus.READY: frozenset({MissionStatus.IN_PROGRESS, MissionStatus.ABORTED}),
    MissionStatus.IN_PROGRESS: frozenset({MissionStatus.COMPLETED, MissionStatus.ABORTED}),
    MissionStatus.COMPLETED: frozenset(),
    MissionStatus.CANCELLED: frozenset(),
    MissionStatus.ABORTED: frozenset(),
}


@dataclass(frozen=True)
class Mission:
    id: str
    country_id: str
    organization_id: str
    status: MissionStatus = MissionStatus.DRAFT
    vehicle_id: str | None = None
    route_id: str | None = None
    corridor_id: str | None = None


def can_transition(current: MissionStatus, target: MissionStatus) -> bool:
    return target in _ALLOWED_TRANSITIONS[current]


def transition(mission: Mission, target: MissionStatus) -> Mission:
    if not can_transition(mission.status, target):
        raise ValueError(f"invalid mission transition: {mission.status} -> {target}")
    return Mission(
        id=mission.id,
        country_id=mission.country_id,
        organization_id=mission.organization_id,
        status=target,
        vehicle_id=mission.vehicle_id,
        route_id=mission.route_id,
        corridor_id=mission.corridor_id,
    )
