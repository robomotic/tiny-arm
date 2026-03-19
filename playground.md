# TinyArm Playground: Miniature Simulation Environments

The **TinyArm Playground** is a sub-project focused on creating 3D-printable, scaled-down versions of real-world environments. These miniature sets allow for low-cost, high-fidelity simulation and training of the **TinyArm** (and other small-scale robots) in scenarios ranging from retail shops to industrial factories.

## Concept
Transform large-scale industrial and commercial spaces into desktop-sized "playgrounds" (typically 1:10 or 1:20 scale) for testing AI models, teleoperation, and automation routines.

## Goals
1.  **Cost-Effective Simulation**: Test complex interactions (sorting, stocking, assembly) without the need for full-scale equipment.
2.  **Rapid Iteration**: Quickly modify environment layouts by printing new components.
3.  **Data Collection for LeRobot**: Provide a consistent and controlled environment for gathering training data using the TinyArm's integrated camera.
4.  **Safe Environment**: Enable experimentation with robotic movements in a safe, miniature setting before deploying to larger systems.

## Target Environments

### 1. The Miniature Shop
A retail simulation environment focusing on object manipulation and logistics.
*   **Key Elements**: 
    *   Modular shelves (adjustable height).
    *   Point-of-Sale (POS) counter.
    *   Small-scale consumer goods (boxes, cans, bags).
    *   Narrow aisles to test navigation and reach.
*   **Use Cases**: Inventory management, shelf stocking automation, and customer interaction scripts.

### 2. The Miniature Factory
An industrial simulation for manufacturing and assembly line testing.
*   **Key Elements**:
    *   Conveyor belt systems (static or motorized).
    *   Workstations with tiny fixtures and jigs.
    *   Storage bins and pallets.
    *   Safety barriers and "warning" zones.
*   **Use Cases**: Pick-and-place routines, quality control inspection, and multi-robot coordination.

## Technical Specifications

| Feature | Specification |
| :--- | :--- |
| **Common Scales** | 1:10 (Standard) or 1:20 (Compact) |
| **Material** | PLA / PETG (Standard), TPU for flexible items |
| **Modularity** | Grid-based floor tiles (e.g., 100mm x 100mm) |
| **Integration** | Mounting points for TinyArm base and XIAO sensors |

## Next Steps
*   [ ] Design a standard set of "shop" assets in OnShape.
*   [ ] Create a grid-based baseplate system for stable environment assembly.
*   [ ] Define a library of miniature "manipulables" (items the robot can grip).
*   [ ] Integrate environment MJC (MuJoCo) files into the LeRobot simulation pipeline.

---
*Building the future of robotics, one miniature factory at a time.*
