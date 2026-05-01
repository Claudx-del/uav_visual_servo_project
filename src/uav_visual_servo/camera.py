from __future__ import annotations

import cv2


class CameraStream:
    """Camera or video file wrapper."""

    def __init__(self, source: int | str = 0, width: int = 640, height: int = 480, fps: int = 30) -> None:
        self.capture = cv2.VideoCapture(source)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.capture.set(cv2.CAP_PROP_FPS, fps)

        if not self.capture.isOpened():
            raise RuntimeError(f"Cannot open camera/video source: {source}")

    def read(self):
        ok, frame = self.capture.read()
        if not ok:
            return None
        return frame

    def release(self) -> None:
        self.capture.release()
