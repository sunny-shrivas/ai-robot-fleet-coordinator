"""Deterministic demo scenario; no physical robot connections."""
from fleet.coordinator import FleetCoordinator
from fleet.grid import GridMap
from fleet.models import Mission, Position, Robot, RobotStatus


def build_demo() -> tuple[FleetCoordinator, Mission]:
    grid = GridMap(
        width=12,
        height=8,
        obstacles={
            Position(4, 1), Position(4, 2), Position(4, 3),
            Position(7, 4), Position(7, 5), Position(7, 6),
        },
    )
    robots = [
        Robot("AMR-01", Position(1, 1), battery_pct=82, max_payload_kg=25),
        Robot("AMR-02", Position(1, 6), battery_pct=56, max_payload_kg=40),
        Robot("AMR-03", Position(10, 1), battery_pct=31, status=RobotStatus.AVAILABLE, max_payload_kg=30),
    ]
    mission = Mission(
        mission_id="MISSION-001",
        pickup=Position(2, 2),
        destination=Position(10, 6),
        payload_kg=12,
        priority=2,
        estimated_energy_pct_per_step=1.1,
        reserve_battery_pct=20,
    )
    return FleetCoordinator(grid, robots), mission
