from __future__ import annotations

from .controller import VelocityCommand


class RosPx4Adapter:
    """Placeholder adapter for ROS/PX4 Offboard control.

    This file gives the project a clear engineering extension point. In a real
    system, replace print_command with ROS2 publishers, such as publishing
    geometry_msgs/TwistStamped or px4_msgs/TrajectorySetpoint.
    """

    def __init__(self) -> None:
        self.connected = False

    def connect(self) -> None:
        # TODO: Initialize ROS2 node and PX4 offboard mode.
        self.connected = True

    def send_velocity(self, command: VelocityCommand) -> None:
        if not self.connected:
            raise RuntimeError("PX4 adapter is not connected")
        self.print_command(command)

    @staticmethod
    def print_command(command: VelocityCommand) -> None:
        print(
            f"PX4 velocity command: vx={command.vx:.3f}, "
            f"vy={command.vy:.3f}, vz={command.vz:.3f}, yaw_rate={command.yaw_rate:.3f}"
        )
