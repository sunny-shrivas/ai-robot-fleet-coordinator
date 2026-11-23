"""Run a deterministic, simulation-only fleet coordination demo."""
import json

from fleet.demo_data import build_demo
from fleet.visualization import render_plan


def run_fleet_system() -> None:
    coordinator, mission = build_demo()
    assignment = coordinator.plan_mission(mission)
    robot = coordinator.robots.get(assignment.robot_id) if assignment.robot_id else None

    print("\n=== AI ROBOT FLEET COORDINATOR ===")
    print("Deterministic planning demo — simulation only; no robot commands are sent.\n")
    print(json.dumps(assignment.to_dict(), indent=2))
    print("\nWarehouse grid:")
    print(render_plan(coordinator.grid, assignment, robot, mission.pickup, mission.destination))


if __name__ == "__main__":
    run_fleet_system()
