import pytest

from fleet.grid import GridMap
from fleet.models import Position


def test_astar_finds_path_around_obstacle():
    grid = GridMap(5, 5, {Position(1, 0), Position(1, 1), Position(1, 2)})
    path = grid.shortest_path(Position(0, 0), Position(3, 0))
    assert path[0] == Position(0, 0)
    assert path[-1] == Position(3, 0)
    assert len(path) - 1 == 9
    assert all(point not in grid.obstacles for point in path)
    assert all(abs(a.x - b.x) + abs(a.y - b.y) == 1 for a, b in zip(path, path[1:]))


def test_start_equal_goal():
    grid = GridMap(2, 2)
    assert grid.shortest_path(Position(0, 0), Position(0, 0)) == [Position(0, 0)]


def test_no_path_raises():
    grid = GridMap(3, 3, {Position(1, 0), Position(1, 1), Position(1, 2)})
    with pytest.raises(ValueError, match="No collision-free path"):
        grid.shortest_path(Position(0, 1), Position(2, 1))


def test_blocked_goal_rejected():
    grid = GridMap(3, 3, {Position(2, 2)})
    with pytest.raises(ValueError, match="blocked"):
        grid.shortest_path(Position(0, 0), Position(2, 2))
