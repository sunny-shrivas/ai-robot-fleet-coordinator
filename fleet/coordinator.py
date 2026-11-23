"""Deterministic robot selection and mission feasibility checks."""
from __future__ import annotations

from fleet.grid import GridMap
from fleet.models import Assignment, Mission, MissionStatus, Position, Robot, RobotStatus


class FleetCoordinator:
    """Plans a single mission against a snapshot of known robot state.

    Selection is lexicographic: shortest feasible total route first, then
    highest projected remaining battery, then stable robot ID. Planning does
    not reserve a robot or mutate telemetry; callers must revalidate state
    before any future dispatch integration.
    """

    def __init__(self, grid: GridMap, robots: list[Robot]):
        self.grid = grid
        self.robots = {robot.robot_id: robot for robot in robots}
        if len(self.robots) != len(robots):
            raise ValueError("Robot IDs must be unique.")

    def plan_mission(self, mission: Mission) -> Assignment:
        candidates: list[tuple[int, float, str, list[Position]]] = []
        rejection_reasons: list[str] = []

        for robot in self.robots.values():
            if robot.status != RobotStatus.AVAILABLE:
                rejection_reasons.append(f"{robot.robot_id}: status is {robot.status.value}")
                continue
            if mission.payload_kg > robot.max_payload_kg:
                rejection_reasons.append(f"{robot.robot_id}: payload exceeds capacity")
                continue

            try:
                to_pickup = self.grid.shortest_path(robot.position, mission.pickup)
                delivery_route = self.grid.shortest_path(mission.pickup, mission.destination)
            except ValueError as exc:
                rejection_reasons.append(f"{robot.robot_id}: {exc}")
                continue

            route = to_pickup + delivery_route[1:]
            steps = len(route) - 1
            energy_required = steps * mission.estimated_energy_pct_per_step
            battery_after = robot.battery_pct - energy_required

            if battery_after < mission.reserve_battery_pct:
                rejection_reasons.append(
                    f"{robot.robot_id}: projected battery {battery_after:.1f}% "
                    f"falls below reserve {mission.reserve_battery_pct:.1f}%"
                )
                continue

            candidates.append((steps, battery_after, robot.robot_id, route))

        if not candidates:
            reason = "; ".join(rejection_reasons) or "No available robots."
            return Assignment(
                mission_id=mission.mission_id,
                robot_id=None,
                status=MissionStatus.REJECTED,
                reason=reason,
            )

        candidates.sort(key=lambda item: (item[0], -item[1], item[2]))
        steps, battery_after, robot_id, route = candidates[0]
        return Assignment(
            mission_id=mission.mission_id,
            robot_id=robot_id,
            status=MissionStatus.READY,
            route=route,
            estimated_steps=steps,
            estimated_battery_after_pct=round(battery_after, 2),
            reason=(
                "Feasible plan generated using the current state snapshot. "
                "No command has been sent to a robot."
            ),
        )
