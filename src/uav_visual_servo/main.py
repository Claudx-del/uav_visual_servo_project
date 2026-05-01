from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from .camera import CameraStream
from .controller import CommandLimiter
from .detector import ColorTargetDetector, draw_detection
from .utils import load_config
from .visual_servo import ImageBasedVisualServo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UAV visual servo demo")
    parser.add_argument("--camera", default="0", help="Camera index or video path")
    parser.add_argument("--config", default="config/default.yaml", help="Path to config yaml")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = int(args.camera) if str(args.camera).isdigit() else args.camera
    cfg = load_config(Path(args.config))

    camera_cfg = cfg["camera"]
    detector_cfg = cfg["detector"]
    servo_cfg = cfg["servo"]

    stream = CameraStream(source, camera_cfg["width"], camera_cfg["height"], camera_cfg["fps"])
    detector = ColorTargetDetector(
        hsv_lower_1=detector_cfg["hsv_lower_1"],
        hsv_upper_1=detector_cfg["hsv_upper_1"],
        hsv_lower_2=detector_cfg.get("hsv_lower_2"),
        hsv_upper_2=detector_cfg.get("hsv_upper_2"),
        min_area=detector_cfg.get("min_area", 200),
    )
    limiter = CommandLimiter(servo_cfg["max_vx"], servo_cfg["max_vy"], servo_cfg["max_vz"])
    servo = ImageBasedVisualServo(
        image_width=camera_cfg["width"],
        image_height=camera_cfg["height"],
        gain_x=servo_cfg["gain_x"],
        gain_y=servo_cfg["gain_y"],
        gain_z=servo_cfg["gain_z"],
        dead_zone=servo_cfg["dead_zone"],
        limiter=limiter,
    )

    try:
        while True:
            frame = stream.read()
            if frame is None:
                break

            detection = detector.detect(frame)
            command = servo.compute_command(detection)

            view = draw_detection(frame, detection)
            cv2.putText(
                view,
                f"cmd vx={command.vx:.2f}, vy={command.vy:.2f}, vz={command.vz:.2f}",
                (20, view.shape[0] - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )
            cv2.imshow("UAV Visual Servo", view)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        stream.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
