"""Typed and validated domain models for the fleet planner."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import math
from typing import Any


def _finite_number(name: str, value: Any, *, minimum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number.")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be a finite number.")
    if minimum is not None and number < minimum:
        raise ValueError(f"{name} must be at least {minimum}.")
    return number


class RobotStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    CHARGING = "charging"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class MissionStatus(str, Enum):
    PLANNED = "planned"
    REJECTED = "rejected"
    READY = "ready"


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __post_init__(self) -> None:
        if (
            isinstance(self.x, bool)
            or isinstance(self.y, bool)
            or not isinstance(self.x, int)
            or not isinstance(self.y, int)
        ):
            raise ValueError("Position coordinates must be integers.")

    @classmethod
    def from_value(cls, value: Any) -> "Position":
        if isinstance(value, cls):
            return value
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError("Position must be a 2-item [x, y] coordinate.")
        return cls(x=value[0], y=value[1])

    def as_list(self) -> list[int]:
        return [self.x, self.y]


@dataclass
class Robot:
    robot_id: str
    position: Position
    battery_pct: float
    status: RobotStatus = RobotStatus.AVAILABLE
    max_payload_kg: float = 20.0
    name: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.robot_id, str) or not self.robot_id.strip():
            raise ValueError("robot_id cannot be empty.")
        battery = _finite_number("battery_pct", self.battery_pct, minimum=0)
        if battery > 100:
            raise ValueError("battery_pct must be between 0 and 100.")
        self.battery_pct = battery

        payload = _finite_number("max_payload_kg", self.max_payload_kg, minimum=0)
        self.max_payload_kg = payload

        try:
            self.status = RobotStatus(self.status)
        except ValueError as exc:
            raise ValueError(f"Unsupported robot status: {self.status}") from exc


@dataclass
class Mission:
    mission_id: str
    pickup: Position
    destination: Position
    payload_kg: float = 0.0
    priority: int = 3
    estimated_energy_pct_per_step: float = 0.8
    reserve_battery_pct: float = 20.0

    def __post_init__(self) -> None:
        if not isinstance(self.mission_id, str) or not self.mission_id.strip():
            raise ValueError("mission_id cannot be empty.")
        self.payload_kg = _finite_number("payload_kg", self.payload_kg, minimum=0)
        if isinstance(self.priority, bool) or not isinstance(self.priority, int) or not 1 <= self.priority <= 5:
            raise ValueError("priority must be an integer between 1 and 5.")
        self.estimated_energy_pct_per_step = _finite_number(
            "estimated_energy_pct_per_step", self.estimated_energy_pct_per_step, minimum=0
        )
        reserve = _finite_number("reserve_battery_pct", self.reserve_battery_pct, minimum=0)
        if reserve > 100:
            raise ValueError("reserve_battery_pct must be between 0 and 100.")
        self.reserve_battery_pct = reserve


@dataclass
class Assignment:
    mission_id: str
    robot_id: str | None
    status: MissionStatus
    route: list[Position] = field(default_factory=list)
    estimated_steps: int = 0
    estimated_battery_after_pct: float | None = None
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "robot_id": self.robot_id,
            "status": self.status.value,
            "route": [point.as_list() for point in self.route],
            "estimated_steps": self.estimated_steps,
            "estimated_battery_after_pct": self.estimated_battery_after_pct,
            "reason": self.reason,
        }
