# 基于视觉感知的无人机智能伺服控制系统

本项目是一个可运行的无人机视觉伺服控制原型系统，核心流程为：

摄像头/视频输入 → 目标检测 → 图像误差计算 → 视觉伺服控制律 → 无人机速度指令输出。

项目默认使用 Python + OpenCV + NumPy 实现，适合用于项目申报、课程设计、科研原型验证或后续接入 ROS/PX4。

## 功能模块

- `detector.py`：基于颜色阈值的目标检测，可替换为 YOLO/深度学习检测器。
- `visual_servo.py`：图像平面视觉伺服控制器，根据目标中心误差输出速度控制量。
- `controller.py`：无人机速度指令封装与限幅。
- `camera.py`：摄像头/视频输入接口。
- `simulator.py`：二维视觉伺服仿真环境，无需真实无人机即可验证控制逻辑。
- `main.py`：实时视觉伺服主程序。
- `ros_px4_adapter.py`：ROS/PX4 接口预留模板。

## 快速运行

```bash
pip install -r requirements.txt
python examples/run_simulation.py
```

若有摄像头，可运行：

```bash
python -m src.uav_visual_servo.main --camera 0
```

## 项目亮点

1. 将图像目标检测结果转化为无人机闭环控制误差。
2. 采用视觉伺服控制律实现目标居中跟踪。
3. 预留 ROS/PX4 接口，便于接入真实飞控系统。
4. 支持仿真验证，可展示控制收敛过程。

## 后续可扩展方向

- 将颜色检测替换为 YOLOv8 / RT-DETR 等深度学习检测模型。
- 引入深度估计或 ArUco 标记实现 6D 位姿估计。
- 接入 ROS2 + PX4 Offboard 控制。
- 加入自适应控制或强化学习参数优化模块。
