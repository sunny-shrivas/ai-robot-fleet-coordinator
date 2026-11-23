from fleet.demo_data import build_demo
from fleet.visualization import render_plan


def test_renderer_marks_route_obstacles_and_mission_points():
    coordinator, mission = build_demo()
    assignment = coordinator.plan_mission(mission)
    robot = coordinator.robots[assignment.robot_id]
    rendered = render_plan(coordinator.grid, assignment, robot, mission.pickup, mission.destination)

    assert "R" in rendered
    assert "P" in rendered
    assert "D" in rendered
    assert "#" in rendered
    assert "*" in rendered
