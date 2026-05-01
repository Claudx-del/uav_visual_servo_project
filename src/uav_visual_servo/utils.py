from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any


def load_config(path: str | Path) -> dict[str, Any]:
    """Load YAML configuration."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a scalar value."""
    return max(min_value, min(max_value, value))
