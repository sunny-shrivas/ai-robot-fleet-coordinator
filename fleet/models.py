"""Typed domain models for the deterministic fleet core."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


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

    @classmethod
    def from_value(cls, value: Any) -> "Position":
        if isinstance(value, cls):
            return value
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError("Position must be a 2-item [x, y] coordinate.")
        x, y = value
        if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Position coordinates must be integers.")
        return cls(x=x, y=y)

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
        if not self.robot_id.strip():
            raise ValueError("robot_id cannot be empty.")
        if not 0 <= self.battery_pct <= 100:
            raise ValueError("battery_pct must be between 0 and 100.")
        if self.max_payload_kg < 0:
            raise ValueError("max_payload_kg cannot be negative.")


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
        if not self.mission_id.strip():
            raise ValueError("mission_id cannot be empty.")
        if self.payload_kg < 0:
            raise ValueError("payload_kg cannot be negative.")
        if not 1 <= self.priority <= 5:
            raise ValueError("priority must be between 1 and 5.")
        if self.estimated_energy_pct_per_step < 0:
            raise ValueError("estimated_energy_pct_per_step cannot be negative.")
        if not 0 <= self.reserve_battery_pct <= 100:
            raise ValueError("reserve_battery_pct must be between 0 and 100.")


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
