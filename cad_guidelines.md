# CAD Design guidelines for TinyArm 101

To ensure that our physical design translates correctly into our simulation environments (MuJoCo, URDF, Three.js), we follow specific guidelines when designing in **Onshape**. These rules are optimized for the [onshape-to-robot](https://onshape-to-robot.readthedocs.io/en/latest/) exporter.

## 1. Top-Level Assembly Structure

The exporter looks for a specific assembly to define the robot.
- **Top-Level Assembly**: Create one assembly that represents the entire robot.
- **Instances as Links**: Each instance in the top-level assembly (whether a Part or a Sub-Assembly) becomes one "Link" in the robot description.
- **Base Link**: The first instance in the assembly list is automatically treated as the **Base Link**.
- **Merging Links**: If you have multiple parts that should be a single rigid link, you can:
    - Put them in a sub-assembly.
    - Use common mates that the exporter will recognize (e.g., `fix_` prefix).

## 2. Defining Degrees of Freedom (DOF)

Joints are defined using **Mate Connectors** with specific naming conventions.

| Prefix | Mate Type | Resulting Joint |
| :--- | :--- | :--- |
| `dof_` | Revolute / Cylindrical | **Revolute Joint** |
| `dof_` | Slider | **Prismatic Joint** |
| `dof_` | Fastened | **Fixed Joint** |

### Key Rules:
- **Z-Axis Alignment**: In Onshape, the **Z-Axis** of the Mate Connector is always the axis of rotation or translation. Ensure your Mate Connector's Z-axis is correctly aligned with the hinge or slider direction.
- **Joint Limits**: Set the limits directly in the Onshape Mate. The exporter will read these and apply them to the URDF/MuJoCo model.
- **Inversion**: If a joint rotates in the opposite direction than desired, append `_inv` (e.g., `dof_shoulder_pitch_inv`).

## 3. Naming Conventions

Consistency in naming simplifies the simulation and control logic.
- **Mates for DOFs**: Name them `dof_<joint_name>` (e.g., `dof_base_yaw`).
- **Link Overrides**: If you want to force a specific name for a link, add a Mate Connector to the part and name it `link_<link_name>`.
- **Custom Frames (Sites)**: To add specific reference points (like the end-effector tip or a sensor mounting point), add a Mate Connector and name it `frame_<frame_name>`.
    - In **MuJoCo**, these become `<site>` elements.
    - In **URDF**, these become dummy links connected by fixed joints.

## 4. Inertia and Physics

- **Mass & Inertia**: By default, the exporter uses Onshape's calculated mass and inertia properties. 
    - Ensure all parts have correctly assigned **Materials** (e.g., PLA for printed parts, Steel for rods).
- **Geometric Simplification**:
    - High-fidelity meshes should be used for **Visual** representation.
    - Simple primitives (boxes, cylinders, spheres) should be used for **Collision** geometry to improve simulation performance and stability. 
    - The `onshape-to-robot` tool can automatically generate simplified collision boxes if configured.

## 5. Visual vs. Collision Meshes

To achieve both high performance and visual excellence:
1.  **Visuals**: Use the full detailed CAD model.
2.  **Collision**: In Onshape, you can create a simplified version of your links (using "Part Studios") that only contains the essential bounding volumes.
3.  **STLs**: Ensure STLs are exported in Meters (if not handled by the exporter script).

## 6. Recommended Workflow

1.  **Design links** in individual Part Studios.
2.  **Assemble links** in a single "Robot Assembly".
3.  **Place Mate Connectors** for every joint, ensuring Z-alignment.
4.  **Rename Mates** using the `dof_` prefix.
5.  **Run the exporter**: Use `onshape-to-robot` to generate the URDF/SDF/MuJoCo assets.
6.  **Verify in Viewer**: Use the [MuJoCo WASM Viewer](web/index.html) or `mujoco/interactive.py` to check joint axes and limits.

---

### Resources
- [Official onshape-to-robot Docs](https://onshape-to-robot.readthedocs.io/en/latest/)
- [Onshape to Robot Tutorial (YouTube)](https://www.youtube.com/watch?v=TJeCpGnX508)
- [MuJoCo Tutorial: Onshape to MuJoCo (YouTube)](https://www.youtube.com/watch?v=L9dAhRa1hCg)
- [URDF Generation (YouTube)](https://www.youtube.com/watch?v=a7KjCUsjt8Y)
- [Building a robot in Onshape (YouTube)](https://www.youtube.com/watch?v=C8oK4uUmbRw)
