# TinyArm 101: 6-DOF Miniature Robotic Arm

A tiny, 3D-printable, open-source robotic arm project inspired by the SO-ARM 101. Designed for **LeRobot** compatibility and based on the **Seeed Studio XIAO** ecosystem.

## Project Overview
This project consists of two replica arms:
1.  **Follower Arm**: 6-DOF (5 Revolute + 1 Gripper) with an integrated tiny camera for AI data collection.
2.  **Leader Arm**: A passive replica used for teleoperation, featuring a spring-loaded trigger to measure grip intensity.

## Hardware Stack
*   **Controller**: [Seeed Studio XIAO ESP32S3 Sense](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5631.html) (Follower) / [XIAO ESP32-C3](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html) (Leader).
*   **Expansion**: [XIAO Expansion Board](https://www.seeedstudio.com/Seeeduino-XIAO-Expansion-board-p-4746.html).
*   **Servos**: **EMAX ES08MA II** (12g, Metal Gear) or **MG90S** (Budget).
*   **Camera**: OV2640 2MP (included with XIAO Sense).
*   **Feedback**: 
    *   **Follower**: None (Open-loop PWM).
    *   **Leader**: Potentiometers in joints + Trigger mechanism for grip.

## Cost Estimate (2-Arm Setup)

| Component | Mid (EMAX ES08MA II) | Budget (MG90S) |
| :--- | :---: | :---: |
| Servos / Pots | $60.00 | $45.00 |
| MCUs (S3 + C3) | $28.00 | $28.00 |
| Expansion Boards | $30.00 | $30.00 |
| Trigger (FSR/Pot) | $10.00 | $10.00 |
| Battery & Power | $24.00 | $24.00 |
| Filament & Misc | $20.00 | $20.00 |
| **Total Est.** | **~$172.00** | **~$157.00** |

## Design & Simulation
*   **Editor**: [OnShape](https://www.onshape.com/) (Open Source Project).
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
