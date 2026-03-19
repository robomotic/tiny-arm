import mujoco
import numpy as np
import os

# MG90S Spec: 0.2 Nm stall.
STALL_LIMIT = 0.20
SAFETY_MARGIN = 0.90 # 90% of stall (0.18 Nm)
GOAL_TORQUE = STALL_LIMIT * SAFETY_MARGIN

def create_temp_xml(l1, l2):
    """Generates an XML with specified lengths for upper arm and forearm."""
    xml_template = f"""
<mujoco model="follower_arm_search">
    <compiler angle="degree" coordinate="local" inertiafromgeom="true"/>
    <default>
        <joint armature="0" damping="0" limited="true"/>
        <geom conaffinity="0" condim="3" density="100" friction="1 0.5 0.5" margin="0.001" rgba="0.2 0.2 0.8 1"/>
        <position kp="1000" forcelimited="true" forcerange="-0.2 0.2" ctrlrange="-180 180"/>
    </default>

    <worldbody>
        <body name="f_base" pos="0 0 0">
            <geom name="f_base_geom" type="cylinder" size="0.03 0.01"/>
            <joint name="f_joint1" type="hinge" axis="0 0 1" range="-170 170"/>
            
            <body name="f_shoulder" pos="0 0 0.02">
                <geom name="f_shoulder_geom" type="box" size="0.015 0.015 0.02"/>
                <joint name="f_joint2" type="hinge" axis="0 1 0" range="-90 90"/>
                
                <body name="f_upper_arm" pos="0 0 0.02">
                    <geom name="f_upper_arm_geom" type="cylinder" size="0.005 {l1/2}" rgba="0.5 0.5 1 1" pos="0 0 {l1/2}"/>
                    <!-- Add mass of elbow servo (13g) -->
                    <body name="f_elbow_servo" pos="0 0 {l1}">
                         <geom type="box" size="0.01 0.01 0.01" rgba="0.3 0.3 0.3 1" mass="0.0134"/>
                         <body name="f_elbow" pos="0 0 0.01">
                            <geom name="f_elbow_geom" type="box" size="0.015 0.015 0.01"/>
                            <joint name="f_joint3" type="hinge" axis="0 1 0" range="-120 120"/>
                            
                            <body name="f_forearm" pos="0 0 0.01">
                                <geom name="f_forearm_geom" type="cylinder" size="0.005 {l2/2}" rgba="0.5 0.5 1 1" pos="0 0 {l2/2}"/>
                                <!-- Add mass of wrist servo (13g) -->
                                <body name="f_wrist_servo" pos="0 0 {l2}">
                                     <geom type="box" size="0.01 0.01 0.01" rgba="0.3 0.3 0.3 1" mass="0.0134"/>
                                     <body name="f_wrist" pos="0 0 0.01">
                                        <geom name="f_wrist_geom" type="box" size="0.01 0.01 0.01"/>
                                        <joint name="f_joint4" type="hinge" axis="0 1 0" range="-90 90"/>
                                     </body>
                                </body>
                            </body>
                         </body>
                    </body>
                </body>
            </body>
        </body>
    </worldbody>

    <actuator>
        <position name="f_motor1" joint="f_joint1"/>
        <position name="f_motor2" joint="f_joint2"/>
        <position name="f_motor3" joint="f_joint3"/>
        <position name="f_motor4" joint="f_joint4"/>
    </actuator>
</mujoco>
"""
    return xml_template

def test_config(l1, l2):
    xml_str = create_temp_xml(l1, l2)
    model = mujoco.MjModel.from_xml_string(xml_str)
    data = mujoco.MjData(model)
    
    # Pose arm horizontally (Shoulder 90 deg, Elbow 0 deg)
    data.ctrl[1] = 90
    data.ctrl[2] = 0
    
    # Step simulation for a bit to stabilize
    # Allow 1000 steps (10 seconds) for damped settling
    for _ in range(1000):
        mujoco.mj_step(model, data)
    
    final_force = np.abs(data.actuator_force[1]) # Shoulder force
    q_reached_rad = data.joint("f_joint2").qpos[0]
    q_target_rad = 90 * np.pi / 180
    
    if abs(q_reached_rad - q_target_rad) > 0.1: # 0.1 rad tolerance
        return False, final_force # Stalled or failed to lift
        
    return (final_force < GOAL_TORQUE), final_force

def run_grid_search():
    l1_range = np.arange(0.04, 0.21, 0.02)
    l2_range = np.arange(0.04, 0.21, 0.02)
    
    best_reach = 0
    best_l1 = 0
    best_l2 = 0
    
    results = []
    
    print(f"Starting Grid Search (Stall Limit: {STALL_LIMIT} Nm, Safe Target: {GOAL_TORQUE} Nm)")
    print("-" * 50)
    
    for l1 in l1_range:
        for l2 in l2_range:
            success, force = test_config(l1, l2)
            print(f"DEBUG {l1:.2f} {l2:.2f}: Success={success}, Force={force:.4f}")
            reach = l1 + l2
            # model_dbg = mujoco.MjModel.from_xml_string(create_temp_xml(l1, l2))
            # data_dbg = mujoco.MjData(model_dbg)
            # data_dbg.ctrl[1] = 90
            # for _ in range(200): mujoco.mj_step(model_dbg, data_dbg)
            # qpos_reached = data_dbg.joint("f_joint2").qpos[0]
            # print(f"DEBUG: L1={l1:.2f}, L2={l2:.2f}, Success={success}, Force={force:.4f}, Qpos={qpos_reached:.2f}")
            if success:
                print(f"SAFE CONFIG: L1={l1*100:.1f}cm, L2={l2*100:.1f}cm, Reach={reach*100:.1f}cm, Torque={force:.4f}Nm")
                if reach > best_reach:
                    best_reach = reach
                    best_l1 = l1
                    best_l2 = l2
            # else:
            #     print(f"L1: {l1:.2f} m, L2: {l2:.2f} m -> STALL ({force:.4f} Nm)")

    print("-" * 50)
    print(f"GRID SEARCH COMPLETE")
    print(f"Optimal Configuration (Longest Safe Reach):")
    print(f"  Upper Arm (L1): {best_l1*100:.1f} cm")
    print(f"  Forearm (L2)  : {best_l2*100:.1f} cm")
    print(f"  Total Reach   : {best_reach*100:.1f} cm")
    print(f"  Safety Margin : {100- (best_reach/0.38)*100:.1f}% approx") # dummy math for display

if __name__ == "__main__":
    run_grid_search()
