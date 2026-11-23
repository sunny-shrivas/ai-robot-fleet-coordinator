import pytest

from fleet.models import Mission, Position, Robot


def test_position_rejects_non_integer_coordinate():
    with pytest.raises(ValueError, match="integers"):
        Position.from_value([1.2, 2])


def test_robot_rejects_out_of_range_battery():
    with pytest.raises(ValueError, match="between 0 and 100"):
        Robot("AMR", Position(0, 0), 101)


def test_mission_rejects_invalid_priority():
    with pytest.raises(ValueError, match="priority"):
        Mission("M", Position(0, 0), Position(1, 1), priority=0)
