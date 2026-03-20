# TinyArm 101: 6-DOF Miniature Robotic Arm

A tiny, 3D-printable, open-source robotic arm project inspired by the **SO-ARM100** by [TheRobotStudio](https://github.com/TheRobotStudio/SO-ARM100). Designed for **LeRobot** compatibility and based on the **Seeed Studio XIAO** ecosystem.

## Project Overview
This project consists of two replica arms:
1.  **Follower Arm**: 6-DOF (5 Revolute + 1 Gripper) with a **24cm reach** (12cm + 12cm) optimized for 50g payload capacity using MG90S/EMAX servos.
2.  **Leader Arm**: A passive replica used for teleoperation, featuring a spring-loaded trigger to measure grip intensity.

## Geometric Specifications
*   **Upper Arm (L1)**: 12.0 cm
*   **Forearm (L2)**: 12.0 cm
*   **Total Reach**: 24.0 cm

## Shoulder Gravity Compensation (Spring Tensor)
To handle the high torque demands at full 24cm extension with a 50g payload, a shoulder **helper spring** (or strong rubber band) is required to reduce servo stress.

*   **Design Goal**: The spring should passively hold the arm at ~45° when unpowered.
*   **Target Stiffness**: $k \approx 0.14 Nm/rad$.
*   **Servo Load Reduction**: **70%** (Peak torque drops from **0.17 Nm** to **0.05 Nm**).
*   **CAD Implementation**: Ensure anchor points are included on the **Base** and **Shoulder (J2)** blocks for mounting an extension spring.

## Hardware Stack
*   **Controller**: [Seeed Studio XIAO ESP32S3 Sense](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5631.html) (Follower) / [XIAO ESP32-C3](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html) (Leader).
*   **Servo Driver**: [Adafruit 16-Channel 12-bit PWM/Servo Driver - PCA9685](https://www.adafruit.com/product/815).
*   **Servos**: **EMAX ES08MA II** (12g, Metal Gear) or **MG90S** (Budget).
*   **Camera**: OV2640 2MP (included with XIAO Sense).
*   **Communication**: I2C (SDA/SCL) from XIAO to PCA9685.

## Power & Voltage
The servos (**EMAX ES08MA II** / **MG90S**) are rated for a strict **4.8V to 6.0V** range.
*   **Optimal Performance**: Running the system at exactly **6.0V** increases the stall torque from ~0.18 Nm to **0.22 Nm** compared to a 5V supply.
*   **Warning**: Do **NOT** provide raw 7.4V (2S LiPo) to the servos or PCA9685. You must use a **High-Current 6V Step-Down Converter (Buck/BEC)** that can handle at least 3A continuous (since each servo can draft ~850mA at stall).

## Cost Estimate (2-Arm Setup)

| Component | Mid (EMAX ES08MA II) | Budget (MG90S) |
| :--- | :---: | :---: |
| Servos / Pots | $60.00 | $45.00 |
| MCUs (S3 + C3) | $28.00 | $28.00 |
| Adafruit PCA9685 | $15.00 | $15.00 |
| Trigger (FSR/Pot) | $10.00 | $10.00 |
| Battery & Power | $24.00 | $24.00 |
| Filament & Misc | $20.00 | $20.00 |
| **Total Est.** | **~$172.00** | **~$157.00** |

## Design & Simulation
*   **Editor**: [OnShape](https://www.onshape.com/) (Open Source Project).
*   **CAD Guidelines**: [CAD Design Guidelines](cad_guidelines.md)
*   **Deliverables**:
    *   `STL`: Ready for 3D printing.
    *   `STEP`: For assembly and modification.
    *   `URDF`: For ROS / Simulation.
    *   `MJC`: MuJoCo XML for LeRobot training.

## Camera Cabling & Durability
To prevent breakage of the fragile OV2640 FPC cable:
*   **Strategy**: The XIAO ESP32S3 Sense is mounted directly on the follower's forearm. This keeps the camera cable static, only moving the robust power and data wires across the arm joints.

## Getting Started
1.  Print the parts from the `stl/` directory.
2.  Assemble using M2 and M3 screws.
3.  Flash the ESP32 firmware in `firmware/`.
4.  Connect to LeRobot via USB Serial.

---
*This project is open-source and part of the LeRobot ecosystem.*
