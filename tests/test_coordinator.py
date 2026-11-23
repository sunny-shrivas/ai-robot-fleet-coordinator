from fleet.coordinator import FleetCoordinator
from fleet.grid import GridMap
from fleet.models import Mission, MissionStatus, Position, Robot, RobotStatus


def mission(**kwargs):
    values = dict(
        mission_id="M-1",
        pickup=Position(1, 0),
        destination=Position(4, 0),
        payload_kg=5,
        estimated_energy_pct_per_step=2,
        reserve_battery_pct=20,
    )
    values.update(kwargs)
    return Mission(**values)


def test_selects_shortest_feasible_route_before_battery_tiebreak():
    grid = GridMap(6, 2)
    robots = [
        Robot("near", Position(0, 0), 65),
        Robot("far", Position(0, 1), 95),
    ]
    assignment = FleetCoordinator(grid, robots).plan_mission(mission())
    assert assignment.robot_id == "near"
    assert assignment.status == MissionStatus.READY
    assert assignment.estimated_steps == 4
    assert assignment.estimated_battery_after_pct == 57
    assert assignment.route[0] == Position(0, 0)
    assert assignment.route[-1] == Position(4, 0)


def test_rejects_robot_below_battery_reserve():
    grid = GridMap(6, 2)
    robots = [Robot("low", Position(0, 0), 30)]
    assignment = FleetCoordinator(grid, robots).plan_mission(
        mission(estimated_energy_pct_per_step=3, reserve_battery_pct=25)
    )
    assert assignment.status == MissionStatus.REJECTED
    assert assignment.robot_id is None
    assert "projected battery" in assignment.reason


def test_rejects_busy_or_payload_incompatible_robot():
    grid = GridMap(6, 2)
    robots = [
        Robot("busy", Position(0, 0), 90, status=RobotStatus.BUSY),
        Robot("small", Position(0, 1), 90, max_payload_kg=2),
    ]
    assignment = FleetCoordinator(grid, robots).plan_mission(mission())
    assert assignment.status == MissionStatus.REJECTED
    assert "status is busy" in assignment.reason
    assert "payload exceeds capacity" in assignment.reason


def test_duplicate_robot_ids_rejected():
    robot = Robot("same", Position(0, 0), 90)
    import pytest
    with pytest.raises(ValueError, match="unique"):
        FleetCoordinator(GridMap(2, 2), [robot, robot])


def test_no_robot_available_returns_rejection():
    assignment = FleetCoordinator(GridMap(2, 2), []).plan_mission(
        mission(pickup=Position(0, 0), destination=Position(1, 1))
    )
    assert assignment.status == MissionStatus.REJECTED
    assert assignment.robot_id is None
    assert assignment.reason == "No available robots."
