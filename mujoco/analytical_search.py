import numpy as np

# MG90S Specs
STALL_TORQUE = 0.20  # Nm
SAFE_TORQUE = 0.18   # Nm (10% Safety Margin)
SERVO_MASS = 0.0134  # kg (13.4g)
G = 9.81             # m/s^2

# Material Specs
RADIUS = 0.005       # 5mm radius
DENSITY = 100        # kg/m^3 (approx for thin plastic structure)
AREA = np.pi * RADIUS**2
MASS_PER_M = DENSITY * AREA # ~0.00785 kg/m

PAYLOAD_MASS = 0.050 # 50g payload goal

def calculate_torque(l1, l2):
    # Weight of segments (unchanged)
    m_l1 = MASS_PER_M * l1
    m_l2 = MASS_PER_M * l2
    
    # 1. Elbow Servo
    t_elbow_servo = SERVO_MASS * G * l1
    
    # 2. Upper Arm segment
    t_l1_segment = m_l1 * G * (l1 / 2)
    
    # 3. Wrist Servo
    t_wrist_servo = SERVO_MASS * G * (l1 + l2)
    
    # 4. Forearm segment
    t_l2_segment = m_l2 * G * (l1 + l2 / 2)
    
    # 5. Payload (at the very end)
    t_payload = PAYLOAD_MASS * G * (l1 + l2)
    
    total_torque = t_elbow_servo + t_l1_segment + t_wrist_servo + t_l2_segment + t_payload
    return total_torque

def run_grid_search():
    l1_range = np.arange(0.04, 0.21, 0.01)
    l2_range = np.arange(0.04, 0.21, 0.01)
    
    best_reach = 0
    best_l1 = 0
    best_l2 = 0
    best_torque = 0
    
    print(f"ANALYTICAL GRID SEARCH (L1/L2 Search Space 4cm-20cm)")
    print(f"Goal: Maximize L1+L2 subject to Shoulder Torque < {SAFE_TORQUE} Nm")
    print("-" * 50)
    
    for l1 in l1_range:
        for l2 in l2_range:
            t = calculate_torque(l1, l2)
            reach = l1 + l2
            
            if t < SAFE_TORQUE:
                if reach > best_reach:
                    best_reach = reach
                    best_l1 = l1
                    best_l2 = l2
                    best_torque = t

    print(f"Optimal Result:")
    print(f"  Upper Arm (L1): {best_l1*100:.1f} cm")
    print(f"  Forearm (L2)  : {best_l2*100:.1f} cm")
    print(f"  Total Reach   : {best_reach*100:.1f} cm")
    print(f"  Steady State Shoulder Torque: {best_torque:.4f} Nm")
    print(f"  Margin to Stall (0.2 Nm): {((0.2-best_torque)/0.2)*100:.1f}%")
    print("-" * 50)

if __name__ == "__main__":
    run_grid_search()
