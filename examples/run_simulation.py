from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from src.uav_visual_servo.simulator import VisualServoSimulator


def main() -> None:
    simulator = VisualServoSimulator()
    history = simulator.run(steps=220)

    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    csv_path = out_dir / "simulation_history.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=history[0].keys())
        writer.writeheader()
        writer.writerows(history)

    steps = [h["step"] for h in history]
    xs = [h["x"] for h in history]
    ys = [h["y"] for h in history]

    plt.figure()
    plt.plot(steps, xs, label="target x")
    plt.plot(steps, ys, label="target y")
    plt.axhline(320, linestyle="--", label="desired x")
    plt.axhline(240, linestyle="--", label="desired y")
    plt.xlabel("step")
    plt.ylabel("image coordinate / pixel")
    plt.title("Visual Servo Convergence")
    plt.legend()
    plt.tight_layout()
    fig_path = out_dir / "visual_servo_convergence.png"
    plt.savefig(fig_path, dpi=200)

    print(f"Saved {csv_path}")
    print(f"Saved {fig_path}")


if __name__ == "__main__":
    main()
