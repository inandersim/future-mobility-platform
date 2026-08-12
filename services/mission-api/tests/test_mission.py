import pytest

from app.mission import Mission, MissionStatus, transition


def test_mission_lifecycle() -> None:
    mission = Mission(id="m1", country_id="tr", organization_id="org1")
    mission = transition(mission, MissionStatus.PLANNING)
    mission = transition(mission, MissionStatus.APPROVED)
    mission = transition(mission, MissionStatus.SCHEDULED)
    mission = transition(mission, MissionStatus.READY)
    mission = transition(mission, MissionStatus.IN_PROGRESS)
    mission = transition(mission, MissionStatus.COMPLETED)
    assert mission.status == MissionStatus.COMPLETED


def test_invalid_mission_transition_is_rejected() -> None:
    mission = Mission(id="m1", country_id="tr", organization_id="org1")
    with pytest.raises(ValueError):
        transition(mission, MissionStatus.IN_PROGRESS)
