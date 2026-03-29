"""
ESC203 - Jinesis Group
Drag Force vs. Wet Leaf Stiction Calculator

Determines whether the air blade's drag force (F_D) can overcome
the static friction (stiction) holding a wet leaf to a rough roof surface.

Physics:
    F_D = 0.5 * rho * v^2 * C_D * A          (aerodynamic drag on leaf)
    F_friction = mu_s * m_leaf * g * cos(theta) (static friction on slope)
    Clearance condition: F_D > F_friction
"""

import numpy as np

# ---- Constants ----
RHO_AIR = 1.225        # kg/m^3  (air density at sea level, 15 C)
G = 9.81               # m/s^2

# ---- Leaf Parameters ----
LEAF_MASS_KG = 0.003          # 3 grams (wet maple leaf)
LEAF_AREA_M2 = 40e-4          # ~40 cm^2 cross-sectional area exposed to airflow
CD_LEAF = 1.28                # drag coefficient (flat plate perpendicular, conservative)

# ---- Surface / Slope Parameters ----
MU_STATIC_WET = 0.45          # static friction coeff, wet leaf on asphalt shingle
ROOF_ANGLE_DEG = 30.0         # degrees

# ---- Air Blade Nozzle Parameters (hair dryer baseline) ----
NOZZLE_VELOCITIES_MS = np.array([5, 10, 15, 20, 25, 30])  # m/s sweep


def drag_force(v, rho=RHO_AIR, cd=CD_LEAF, a=LEAF_AREA_M2):
    """Aerodynamic drag force on the leaf."""
    return 0.5 * rho * v**2 * cd * a


def stiction_force(m=LEAF_MASS_KG, mu=MU_STATIC_WET, theta_deg=ROOF_ANGLE_DEG):
    """Static friction force holding the wet leaf on the slope."""
    theta = np.radians(theta_deg)
    normal_force = m * G * np.cos(theta)
    return mu * normal_force


def main():
    f_stiction = stiction_force()

    print("=" * 60)
    print("Jinesis Group - Drag Force vs. Wet Leaf Stiction Analysis")
    print("=" * 60)
    print(f"\nLeaf mass:          {LEAF_MASS_KG * 1000:.1f} g")
    print(f"Leaf area:          {LEAF_AREA_M2 * 1e4:.1f} cm^2")
    print(f"Drag coefficient:   {CD_LEAF}")
    print(f"Friction coeff:     {MU_STATIC_WET}")
    print(f"Roof angle:         {ROOF_ANGLE_DEG} deg")
    print(f"\nStiction force:     {f_stiction * 1000:.2f} mN")
    print()
    print(f"{'v (m/s)':>8}  {'F_D (mN)':>10}  {'F_D/F_stiction':>14}  {'Clears?':>8}")
    print("-" * 48)

    for v in NOZZLE_VELOCITIES_MS:
        fd = drag_force(v)
        ratio = fd / f_stiction
        clears = "YES" if fd > f_stiction else "no"
        print(f"{v:>8.1f}  {fd * 1000:>10.2f}  {ratio:>14.2f}  {clears:>8}")

    # Find minimum velocity to clear
    # F_D = F_stiction  =>  v = sqrt(2 * F_stiction / (rho * CD * A))
    v_min = np.sqrt(2 * f_stiction / (RHO_AIR * CD_LEAF * LEAF_AREA_M2))
    print(f"\nMinimum air velocity to overcome stiction: {v_min:.2f} m/s")
    print(f"  (= {v_min * 3.6:.1f} km/h)")


if __name__ == "__main__":
    main()
