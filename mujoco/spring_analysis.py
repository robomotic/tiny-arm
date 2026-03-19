import numpy as np

# Specs for 12cm + 12cm arm
L1 = 0.12 # m
L2 = 0.12 # m
STALL_TORQUE = 0.20 # Nm
G = 9.81
SERVO_MASS = 0.0134
DENSITY = 100
RADIUS = 0.005
AREA = np.pi * RADIUS**2
MASS_PER_M = DENSITY * AREA
PAYLOAD_MASS = 0.050 # 50g

def get_gravity_torque(angle_deg):
    angle_rad = np.deg2rad(angle_deg)
    # Cos(angle_rad) because torque is max at 90 deg (horizontal)
    # But wait, in our model, 0 is vertical UP.
    # So 90 is horizontal. SIN(angle_rad) is correct if 0 is vertical.
    # Actually let's use SIN(angle_rad) where 90 is horizontal.
    
    m_l1 = MASS_PER_M * L1
    m_l2 = MASS_PER_M * L2
    
    # Lever arms relative to shoulder (Joint 2)
    # T = g * sin(theta) * sum(m_i * r_i)
    moments = (
        SERVO_MASS * L1 +               # Elbow Servo
        m_l1 * (L1 / 2) +               # Upper Arm
        SERVO_MASS * (L1 + L2) +        # Wrist Servo
        m_l2 * (L1 + L2 / 2) +          # Forearm
        PAYLOAD_MASS * (L1 + L2)        # Payload
    )
    
    return moments * G * np.sin(angle_rad)

def analyze_spring():
    angles = np.linspace(0, 90, 100) # 0 to 90 degrees (vertical to horizontal)
    g_torques = [get_gravity_torque(a) for a in angles]
    
    # Optimal spring would roughly balance mid-range or peak.
    # Let's say we want to balance the arm at 45 degrees.
    # T_spring = k * theta_rad
    # k = T_g(45) / deg2rad(45)
    
    k_optimal = get_gravity_torque(60) / np.deg2rad(60)
    
    s_torques = [k_optimal * np.deg2rad(a) for a in angles]
    net_torques = [abs(g - s) for g, s in zip(g_torques, s_torques)]
    
    peak_no_spring = max(g_torques)
    peak_with_spring = max(net_torques)
    reduction = (peak_no_spring - peak_with_spring) / peak_no_spring * 100
    
    print(f"SPRING ANALYSIS (L1=12cm, L2=12cm, Payload=50g)")
    print("-" * 50)
    print(f"Peak Gravity Torque (at 90 deg): {peak_no_spring:.4f} Nm")
    print(f"MG90S Stall Limit             : {STALL_TORQUE:.4f} Nm")
    print(f"Estimated Spring Stiffness (k): {k_optimal:.4f} Nm/rad")
    print(f"New Peak Torque (Servo load)  : {peak_with_spring:.4f} Nm")
    print(f"TORQUE REDUCTION              : {reduction:.1f}%")
    print("-" * 50)
    
    if peak_with_spring < 0.15:
        print("RESULT: Highly Effective. The servo now operates well within comfort limits.")
    else:
        print("RESULT: Helpful, but still close to limits.")

if __name__ == "__main__":
    analyze_spring()
