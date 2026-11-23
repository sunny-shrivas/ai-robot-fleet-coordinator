"""Run the deterministic AI Robot Fleet Coordinator demonstration."""
import json

from fleet.demo_data import build_demo


def run_fleet_system() -> None:
    coordinator, mission = build_demo()
    assignment = coordinator.plan_mission(mission)
    print("\n=== AI ROBOT FLEET COORDINATOR ===")
    print("Deterministic planning demo — simulation only; no robot commands are sent.\n")
    print(json.dumps(assignment.to_dict(), indent=2))


if __name__ == "__main__":
    run_fleet_system()
