from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .detector import Detection
from .visual_servo import ImageBasedVisualServo


@dataclass
class SimState:
    target_x: float
    target_y: float
    target_area: float


class VisualServoSimulator:
    """Simple image-plane simulator for validating visual servo convergence."""

    def __init__(self, width: int = 640, height: int = 480, dt: float = 0.05) -> None:
        self.width = width
        self.height = height
        self.dt = dt
        self.state = SimState(target_x=110.0, target_y=350.0, target_area=9000.0)
        self.servo = ImageBasedVisualServo(width, height)

    def step(self) -> tuple[SimState, object]:
        detection = Detection(
            center_x=self.state.target_x,
            center_y=self.state.target_y,
            area=self.state.target_area,
            bbox=(0, 0, 0, 0),
        )
        command = self.servo.compute_command(detection)

        # 简化图像运动模型：无人机速度改变目标在图像中的相对位置。
        self.state.target_x -= command.vy * 120.0 * self.dt
        self.state.target_y += command.vz * 120.0 * self.dt
        self.state.target_area += command.vx * 6000.0 * self.dt

        self.state.target_x = float(np.clip(self.state.target_x, 0, self.width))
        self.state.target_y = float(np.clip(self.state.target_y, 0, self.height))
        self.state.target_area = float(np.clip(self.state.target_area, 1000, 60000))
        return self.state, command

    def run(self, steps: int = 200):
        history = []
        for k in range(steps):
            state, command = self.step()
            history.append(
                {
                    "step": k,
                    "x": state.target_x,
                    "y": state.target_y,
                    "area": state.target_area,
                    "vx": command.vx,
                    "vy": command.vy,
                    "vz": command.vz,
                }
            )
        return history
