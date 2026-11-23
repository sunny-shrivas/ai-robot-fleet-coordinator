import math
import pytest

from fleet.models import Mission, Position, Robot


def test_position_rejects_non_integer_coordinates():
    with pytest.raises(ValueError, match="integers"):
        Position(1.2, 2)


def test_position_rejects_boolean_coordinates():
    with pytest.raises(ValueError, match="integers"):
        Position(True, 2)


@pytest.mark.parametrize("battery", [101, -1, math.nan, math.inf])
def test_robot_rejects_invalid_battery(battery):
    with pytest.raises(ValueError):
        Robot("AMR", Position(0, 0), battery)


def test_mission_rejects_invalid_priority():
    with pytest.raises(ValueError, match="priority"):
        Mission("M", Position(0, 0), Position(1, 1), priority=0)


def test_mission_rejects_non_finite_energy_estimate():
    with pytest.raises(ValueError, match="finite"):
        Mission("M", Position(0, 0), Position(1, 1), estimated_energy_pct_per_step=math.nan)
