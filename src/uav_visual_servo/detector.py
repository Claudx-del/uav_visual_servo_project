from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np


@dataclass
class Detection:
    center_x: float
    center_y: float
    area: float
    bbox: tuple[int, int, int, int]


class ColorTargetDetector:
    """Detect a colored target in an image using HSV thresholding.

    This detector is intentionally lightweight for demonstration. In a real UAV
    project, this class can be replaced by a neural network detector while
    keeping the same Detection output interface.
    """

    def __init__(
        self,
        hsv_lower_1: list[int],
        hsv_upper_1: list[int],
        hsv_lower_2: list[int] | None = None,
        hsv_upper_2: list[int] | None = None,
        min_area: float = 200,
    ) -> None:
        self.lower_1 = np.array(hsv_lower_1, dtype=np.uint8)
        self.upper_1 = np.array(hsv_upper_1, dtype=np.uint8)
        self.lower_2 = np.array(hsv_lower_2, dtype=np.uint8) if hsv_lower_2 else None
        self.upper_2 = np.array(hsv_upper_2, dtype=np.uint8) if hsv_upper_2 else None
        self.min_area = float(min_area)

    def detect(self, frame: np.ndarray) -> Optional[Detection]:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_1, self.upper_1)

        if self.lower_2 is not None and self.upper_2 is not None:
            mask_2 = cv2.inRange(hsv, self.lower_2, self.upper_2)
            mask = cv2.bitwise_or(mask, mask_2)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(contour)
        if area < self.min_area:
            return None

        x, y, w, h = cv2.boundingRect(contour)
        moments = cv2.moments(contour)
        if moments["m00"] == 0:
            return None

        cx = moments["m10"] / moments["m00"]
        cy = moments["m01"] / moments["m00"]
        return Detection(center_x=cx, center_y=cy, area=area, bbox=(x, y, w, h))


def draw_detection(frame: np.ndarray, detection: Detection | None) -> np.ndarray:
    output = frame.copy()
    if detection is None:
        cv2.putText(output, "Target lost", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        return output

    x, y, w, h = detection.bbox
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.circle(output, (int(detection.center_x), int(detection.center_y)), 5, (255, 0, 0), -1)
    cv2.putText(output, f"area={detection.area:.0f}", (x, max(20, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return output
