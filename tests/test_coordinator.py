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


def test_selects_feasible_robot_with_best_battery_then_route():
    grid = GridMap(6, 2)
    robots = [
        Robot("low", Position(0, 0), 30),
        Robot("high", Position(0, 1), 90),
    ]
    assignment = FleetCoordinator(grid, robots).plan_mission(mission())
    assert assignment.robot_id == "high"
    assert assignment.status == MissionStatus.READY
    assert assignment.route[0] == Position(0, 1)
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
    with __import__("pytest").raises(ValueError, match="unique"):
        FleetCoordinator(GridMap(2, 2), [robot, robot])
