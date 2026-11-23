"""Tiny text renderer for inspecting a planned route in the terminal."""
from __future__ import annotations

from fleet.grid import GridMap
from fleet.models import Assignment, MissionStatus, Position, Robot


def render_plan(
    grid: GridMap,
    assignment: Assignment,
    robot: Robot | None,
    pickup: Position,
    destination: Position,
) -> str:
    route = set(assignment.route)
    rows: list[str] = []
    for y in range(grid.height):
        cells: list[str] = []
        for x in range(grid.width):
            point = Position(x, y)
            if point in grid.obstacles:
                char = "#"
            elif point == destination:
                char = "D"
            elif point == pickup:
                char = "P"
            elif robot is not None and point == robot.position:
                char = "R"
            elif point in route:
                char = "*"
            else:
                char = "."
            cells.append(char)
        rows.append(" ".join(cells))
    return "\n".join(rows) + "\n\nLegend: R robot · P pickup · D destination · * route · # obstacle"
