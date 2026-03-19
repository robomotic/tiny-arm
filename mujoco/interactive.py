import mujoco
from mujoco import viewer
import os
import time
import sys

def run_interactive():
    target = "follower_arm.xml"
    if len(sys.argv) > 1 and "leader" in sys.argv[1].lower():
        target = "leader_arm.xml"
        
    xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), target))
    
    print(f"Loading {target} into interactive viewer...")
    
    # Load model and data
    model = mujoco.MjModel.from_xml_path(xml_path)
    data = mujoco.MjData(model)

    # Launch the interactive viewer
    with viewer.launch_passive(model, data) as viewer_ui:
        print("Interactive Viewer launched!")
        print("Use the 'Control' panel on the right side of the viewer to drag sliders and move the joints.")
        print("Close the window when done.")
        
        while viewer_ui.is_running():
            step_start = time.time()
            mujoco.mj_step(model, data)
            viewer_ui.sync()
            
            time_until_next_step = model.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)

if __name__ == "__main__":
    run_interactive()
