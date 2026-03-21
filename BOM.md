# TinyArm 101: Bill of Materials (BOM)

This document lists the required electronic components for both the **Follower** and **Leader** arms.

## 1. Follower Arm (Actuated)
The Follower arm uses a hybrid servo setup (MG995 + MG90S) to balance high torque at the base with weight efficiency at the end-effector.

| Component | Qty | Role | Link |
| :--- | :---: | :--- | :--- |
| [**MG995 Servo**](https://www.aliexpress.com/item/1005006763630856.html) | 2 | Base (J1) & Shoulder (J2) | [AliExpress](https://www.aliexpress.com/item/1005006763630856.html) |
| [**MG90S Servo**](https://www.aliexpress.com/item/1005008490187744.html) | 4 | Elbow (J3), Wrist (J4/J5), Gripper | [AliExpress](https://www.aliexpress.com/item/1005008490187744.html) |
| [**Power Board**](https://www.aliexpress.com/item/1005011682227241.html) | 1 | 5V/6V High Current Distribution | [AliExpress](https://www.aliexpress.com/item/1005011682227241.html) |
| [**ESP32-S3 Kit**](https://www.aliexpress.com/item/1005009663706482.html) | 1 | DevBoard / Controller Core | [AliExpress](https://www.aliexpress.com/item/1005009663706482.html) |
| **6V 10A PSU** | 1 | Main DC Power Supply | - |

---

## 2. Leader Arm (Passive/Sensor)
The Leader arm is a 1:1 replica of the follower. It uses servos primarily for their internal potentiometers and structural bearings.

| Component | Qty | Role | Link |
| :--- | :---: | :--- | :--- |
| [**MG90S Servo**](https://www.aliexpress.com/item/1005008490187744.html) | 6 | All Joints (Passive Sensors) | [AliExpress](https://www.aliexpress.com/item/1005008490187744.html) |
| [**ESP32-S3 Kit**](https://www.aliexpress.com/item/1005009663706482.html) | 1 | Sensor Data Processing | [AliExpress](https://www.aliexpress.com/item/1005009663706482.html) |
| **Springs** | 2 | Gravity Compensation / Feedback | - |

---

## 3. Structural & Fasteners
- **3D Printed Parts**: Approx. 400g of PETG or PLA+.
- **F623ZZ Bearings**: 4x for the shoulder assembly.
- **M3 Hardware**: Assorted lengths (8mm, 12mm, 20mm).
- **Shoulder Spring**: $k \approx 0.14$ Nm/rad helper spring.
