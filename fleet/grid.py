"""Small deterministic 4-connected grid planner using A*."""
from __future__ import annotations

import heapq
from itertools import count

from fleet.models import Position


class GridMap:
    def __init__(self, width: int, height: int, obstacles: set[Position] | None = None):
        if width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive.")
        self.width = width
        self.height = height
        self.obstacles = obstacles or set()
        for point in self.obstacles:
            if not self.in_bounds(point):
                raise ValueError(f"Obstacle outside grid: {point}")

    def in_bounds(self, point: Position) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def is_free(self, point: Position) -> bool:
        return self.in_bounds(point) and point not in self.obstacles

    @staticmethod
    def _heuristic(a: Position, b: Position) -> int:
        return abs(a.x - b.x) + abs(a.y - b.y)

    def neighbors(self, point: Position) -> list[Position]:
        candidates = [
            Position(point.x + 1, point.y),
            Position(point.x - 1, point.y),
            Position(point.x, point.y + 1),
            Position(point.x, point.y - 1),
        ]
        return sorted((p for p in candidates if self.is_free(p)), key=lambda p: (p.y, p.x))

    def shortest_path(self, start: Position, goal: Position) -> list[Position]:
        if not self.is_free(start):
            raise ValueError(f"Start position is blocked or outside grid: {start}")
        if not self.is_free(goal):
            raise ValueError(f"Goal position is blocked or outside grid: {goal}")
        if start == goal:
            return [start]

        sequence = count()
        frontier: list[tuple[int, int, Position]] = []
        heapq.heappush(frontier, (self._heuristic(start, goal), next(sequence), start))
        came_from: dict[Position, Position | None] = {start: None}
        cost_so_far: dict[Position, int] = {start: 0}

        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current == goal:
                break
            for neighbor in self.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if new_cost < cost_so_far.get(neighbor, 10**12):
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    priority = new_cost + self._heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, next(sequence), neighbor))

        if goal not in came_from:
            raise ValueError("No collision-free path exists on the configured grid.")

        path: list[Position] = []
        current: Position | None = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
