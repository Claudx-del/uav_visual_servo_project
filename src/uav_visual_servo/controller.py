from __future__ import annotations

from dataclasses import dataclass

from .utils import clamp


@dataclass
class VelocityCommand:
    """Body-frame velocity command for UAV control."""

    vx: float
    vy: float
    vz: float
    yaw_rate: float = 0.0


class CommandLimiter:
    """Limit velocity commands to safe bounds."""

    def __init__(self, max_vx: float, max_vy: float, max_vz: float, max_yaw_rate: float = 1.0) -> None:
        self.max_vx = abs(max_vx)
        self.max_vy = abs(max_vy)
        self.max_vz = abs(max_vz)
        self.max_yaw_rate = abs(max_yaw_rate)

    def limit(self, command: VelocityCommand) -> VelocityCommand:
        return VelocityCommand(
            vx=clamp(command.vx, -self.max_vx, self.max_vx),
            vy=clamp(command.vy, -self.max_vy, self.max_vy),
            vz=clamp(command.vz, -self.max_vz, self.max_vz),
            yaw_rate=clamp(command.yaw_rate, -self.max_yaw_rate, self.max_yaw_rate),
        )
