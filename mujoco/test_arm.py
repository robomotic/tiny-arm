import mujoco
import numpy as np
import os
import time

def run_test():
    # Construct absolute path to the XML
    xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "follower_arm.xml"))
    
    # Load model
    print(f"Loading model from {xml_path}...")
    model = mujoco.MjModel.from_xml_path(xml_path)
    data = mujoco.MjData(model)

    # 1. Test Collision Detection
    print("\n--- TEST: Collision Detection ---")
    # Send Joint 2 (Shoulder) and Joint 3 (Elbow) into a self-collision pose
    data.ctrl[1] = 90  # Force shoulder pitch
    data.ctrl[2] = -90 # Force elbow pitch into the base
    
    # Step simulation for a few ticks
    for _ in range(100):
        mujoco.mj_step(model, data)
    
    num_contacts = data.ncon
    print(f"Num contacts detected in collision pose: {num_contacts}")
    if num_contacts > 0:
        for i in range(num_contacts):
            contact = data.contact[i]
            print(f"  Contact {i} between Geoms {contact.geom1} ({model.geom(contact.geom1).name}) and {contact.geom2} ({model.geom(contact.geom2).name})")

    # 2. Test Torque & Stall (MG90S @ 0.2 Nm)
    print("\n--- TEST: Torque & Stall Limits ---")
    # Reset pose
    mujoco.mj_resetData(model, data)
    
    # Target joint 2 (Shoulder) to move against gravity with a payload
    # Let's see the peak torque (actuator force) required to hold position
    data.ctrl[1] = 45 # Try to lift arm to 45 deg
    
    # Monitor for 200 ms (approx 20 steps with 0.01 timestep)
    max_torque = 0
    for t in range(50):
        mujoco.mj_step(model, data)
        current_torque = np.max(np.abs(data.actuator_force))
        max_torque = max(max_torque, current_torque)
        
    print(f"Recorded Peak Torque during move: {max_torque:.4f} Nm")
    print(f"Stall Limit (Target): 0.2 Nm")
    
    if max_torque > 0.18:
        print("WARNING: Approaching stall limit!")
    else:
        print("Torque headroom is sufficient for movement.")

    # 3. Rest Torque (Static Hold)
    print("\n--- TEST: Rest Torque (Static Hold) ---")
    # Let the arm settle at 0 deg (resting pos)
    data.ctrl[:] = 0
    for _ in range(100):
        mujoco.mj_step(model, data)
    
    rest_torque = np.max(np.abs(data.actuator_force))
    print(f"Rest/Stall torque (unloaded hold): {rest_torque:.4f} Nm")

if __name__ == "__main__":
    run_test()
