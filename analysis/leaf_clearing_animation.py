"""
ESC203 - Jinesis Group
Clearer Visualization: Leaf Clearing Simulation based on Prototype

This script creates a highly visual, intuitive plot showing how the
air blade interacts with a sloped roof (mimicking the prototype)
and calculates the clearing zone where stiction is overcome.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import matplotlib.colors as mcolors

# Prototype Parameters
ROOF_ANGLE_DEG = 15.0       # Angle of the roof prototype
ROOF_LENGTH = 0.6           # 60cm track length
NOZZLE_HEIGHT = 0.05        # 5cm above the roof
NOZZLE_ANGLE_DEG = 30.0     # 30 degrees attack angle
AIR_VELOCITY = 25.0         # m/s from hairdryer

# Leaf & Physics Parameters
LEAF_STICTION_FORCE = 0.02  # Newtons (estimated wet leaf holding force)
RHO_AIR = 1.225             # kg/m^3
C_DRAG = 1.1                # Drag coefficient of a wet flat leaf
LEAF_AREA = 0.005           # m^2 cross sectional area exposed

# Generate Grid representing the sloped roof
x_roof = np.linspace(0, ROOF_LENGTH, 500)
y_roof = x_roof * np.tan(np.radians(ROOF_ANGLE_DEG))

# Jet centerline (originating from the nozzle moving along track)
nozzle_x = 0.1
nozzle_y = nozzle_x * np.tan(np.radians(ROOF_ANGLE_DEG)) + NOZZLE_HEIGHT

# Calculate Velocity Decay along the roof surface
# Simplified free jet expansion model intersecting a boundary
distance_from_nozzle = np.sqrt((x_roof - nozzle_x)**2 + (y_roof - nozzle_y)**2)
# The jet loses velocity as it expands. V = V0 * sqrt(Standoff / Distance)
velocity_at_surface = np.zeros_like(distance_from_nozzle)
impact_point_x = nozzle_x + NOZZLE_HEIGHT / np.tan(np.radians(NOZZLE_ANGLE_DEG))

for i, x in enumerate(x_roof):
    if x < nozzle_x:
        velocity_at_surface[i] = 0 # Behind the nozzle
    elif x < impact_point_x:
        velocity_at_surface[i] = AIR_VELOCITY * (x - nozzle_x) / (impact_point_x - nozzle_x) # Ramping up to impact
    else:
        # Decaying after impact due to boundary layer expansion
        velocity_at_surface[i] = AIR_VELOCITY * np.sqrt(0.05 / np.clip(distance_from_nozzle[i], 0.01, None))

velocity_at_surface = np.clip(velocity_at_surface, 0, AIR_VELOCITY)

# Calculate Drag Force applied to leaves at each point on the roof
# F_d = 0.5 * rho * V^2 * Cd * A
drag_force_applied = 0.5 * RHO_AIR * (velocity_at_surface**2) * C_DRAG * LEAF_AREA

# Determine "Clearing Zone" (where Drag Force > Stiction Force)
clearing_zone = drag_force_applied > LEAF_STICTION_FORCE

# --- PLOTTING ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [2, 1]})

# --- Plot 1: Physical System Layout ---
ax1.set_title("Prototype Layout & Air Blade Interaction", fontsize=14, fontweight='bold')
ax1.set_xlim(0, ROOF_LENGTH)
ax1.set_ylim(0, ROOF_LENGTH * np.tan(np.radians(ROOF_ANGLE_DEG)) + 0.15)

# Draw Roof
ax1.plot(x_roof, y_roof, color='#4a4a4a', linewidth=8, label="Sloped Roof (Sandpaper/Shingle)")

# Draw Nozzle
nozzle_poly = Polygon(
    [[nozzle_x-0.02, nozzle_y+0.03], [nozzle_x+0.02, nozzle_y+0.03], [nozzle_x+0.01, nozzle_y], [nozzle_x-0.01, nozzle_y]], 
    closed=True, color='silver', ec='black', label="Moving Air Nozzle"
)
ax1.add_patch(nozzle_poly)

# Draw Airflow cone (Visualizing the jet)
jet_cone_x = [nozzle_x, impact_point_x - 0.05, impact_point_x + 0.2, nozzle_x]
jet_cone_y = [nozzle_y, np.interp(impact_point_x - 0.05, x_roof, y_roof), np.interp(impact_point_x + 0.2, x_roof, y_roof), nozzle_y]
ax1.fill(jet_cone_x, jet_cone_y, color='cyan', alpha=0.3, label="Airflow Jet")

# Highlight Clearing Zone on the roof
ax1.fill_between(x_roof, y_roof, y_roof+0.01, where=clearing_zone, color='lime', alpha=0.8, label="Active Clearing Zone (Leaves Removed)")
ax1.fill_between(x_roof, y_roof, y_roof+0.01, where=~clearing_zone, color='darkorange', alpha=0.5, label="Stiction > Drag (Leaves Remain)")

# Draw some hypothetical leaves
for lx in [0.2, 0.25, 0.35, 0.45, 0.55]:
    ly = np.interp(lx, x_roof, y_roof)
    if drag_force_applied[np.argmin(np.abs(x_roof - lx))] > LEAF_STICTION_FORCE:
        # Leaf being blown away
        ax1.plot(lx+0.02, ly+0.03, marker='o', markersize=8, color='green', alpha=0.6)
        ax1.arrow(lx, ly, 0.02, 0.03, head_width=0.01, color='green', alpha=0.6)
    else:
        # Leaf stuck
        ax1.plot(lx, ly+0.005, marker='o', markersize=8, color='darkgreen')

ax1.set_xlabel("Track Distance (m)")
ax1.set_ylabel("Height (m)")
ax1.legend(loc='upper left', fontsize=9)
ax1.grid(True, linestyle='--', alpha=0.5)

# --- Plot 2: Force Analysis ---
ax2.set_title("Force Analysis Along Track", fontsize=12)
ax2.plot(x_roof, drag_force_applied, color='blue', linewidth=2, label="Applied Drag Force (Air Blade)")
ax2.axhline(LEAF_STICTION_FORCE, color='red', linestyle='--', linewidth=2, label="Wet Leaf Stiction Force (Threshold)")

# Fill the success area
ax2.fill_between(x_roof, drag_force_applied, LEAF_STICTION_FORCE, where=clearing_zone, color='lime', alpha=0.3)

ax2.set_xlabel("Track Distance (m)")
ax2.set_ylabel("Force (Newtons)")
ax2.set_xlim(0, ROOF_LENGTH)
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("prototype_clear_visualization.png", dpi=200)
print("Saved clearer visualization to prototype_clear_visualization.png")
