from __future__ import annotations

from dataclasses import dataclass

from .controller import CommandLimiter, VelocityCommand
from .detector import Detection


@dataclass
class ServoError:
    ex: float
    ey: float
    area_error: float


class ImageBasedVisualServo:
    """Image-based visual servo controller.

    The target is controlled toward the center of the image. The image error is
    normalized into [-1, 1], making the controller independent of image size.
    """

    def __init__(
        self,
        image_width: int,
        image_height: int,
        gain_x: float = 0.8,
        gain_y: float = 0.8,
        gain_z: float = 0.4,
        desired_area_ratio: float = 0.08,
        dead_zone: float = 0.02,
        limiter: CommandLimiter | None = None,
    ) -> None:
        self.image_width = image_width
        self.image_height = image_height
        self.gain_x = gain_x
        self.gain_y = gain_y
        self.gain_z = gain_z
        self.desired_area = desired_area_ratio * image_width * image_height
        self.dead_zone = dead_zone
        self.limiter = limiter or CommandLimiter(1.0, 1.0, 0.6)

    def compute_error(self, detection: Detection) -> ServoError:
        cx_des = self.image_width / 2.0
        cy_des = self.image_height / 2.0
        ex = (detection.center_x - cx_des) / cx_des
        ey = (detection.center_y - cy_des) / cy_des
        area_error = (self.desired_area - detection.area) / max(self.desired_area, 1.0)
        return ServoError(ex=ex, ey=ey, area_error=area_error)

    def compute_command(self, detection: Detection | None) -> VelocityCommand:
        if detection is None:
            # 目标丢失时保持悬停；真实系统可加入搜索策略。
            return VelocityCommand(0.0, 0.0, 0.0, 0.0)

        error = self.compute_error(detection)
        ex = 0.0 if abs(error.ex) < self.dead_zone else error.ex
        ey = 0.0 if abs(error.ey) < self.dead_zone else error.ey
        ez = 0.0 if abs(error.area_error) < self.dead_zone else error.area_error

        # 坐标约定：目标在图像右侧时，机体向右修正；目标在图像下方时，机体向下/降低修正。
        command = VelocityCommand(
            vx=self.gain_z * ez,
            vy=self.gain_x * ex,
            vz=-self.gain_y * ey,
            yaw_rate=0.0,
        )
        return self.limiter.limit(command)
