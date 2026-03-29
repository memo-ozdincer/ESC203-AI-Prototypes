"""
ESC204 - Jinesis Group
Apex Nozzle Visualization: Top-Down Air Blade from Roof Peak

The nozzle is positioned at the APEX (top peak) of a sloped roof,
blowing air downward along the slope. The roof slopes from the apex
(x=0, y=high) downward. Leaves are cleared as the jet travels
down the slope, overcoming wet-leaf stiction.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ── Prototype Parameters ──
ROOF_ANGLE_DEG = 15.0        # Roof slope angle from horizontal
ROOF_LENGTH = 0.6            # 60 cm slope length
NOZZLE_HEIGHT = 0.05         # 5 cm above roof surface at apex
AIR_VELOCITY = 25.0          # m/s exit velocity

# ── Leaf & Physics Parameters ──
LEAF_STICTION_FORCE = 0.02   # N – estimated wet leaf holding force
RHO_AIR = 1.225              # kg/m³
C_DRAG = 1.1                 # Drag coefficient (wet flat leaf)
LEAF_AREA = 0.005            # m² cross-sectional area exposed

# ── Roof Geometry (apex at top-left, slopes down to the right) ──
slope_dist = np.linspace(0, ROOF_LENGTH, 500)          # distance along slope from apex
slope_rad = np.radians(ROOF_ANGLE_DEG)

# World coordinates: apex is at (0, ROOF_LENGTH * sin(slope))
apex_height = ROOF_LENGTH * np.sin(slope_rad)
x_roof = slope_dist * np.cos(slope_rad)
y_roof = apex_height - slope_dist * np.sin(slope_rad)  # descends from apex

# ── Nozzle at the apex, aimed down along the slope ──
nozzle_x = 0.0
nozzle_y = y_roof[0] + NOZZLE_HEIGHT                   # just above apex

# Velocity model: jet exits nozzle, hits roof surface near apex, then
# spreads as a wall jet flowing down the slope.
# Near the nozzle the jet hasn't fully developed; after attachment it
# decays with distance as V = V0 * sqrt(d0 / d) (free-jet decay).
STANDOFF = NOZZLE_HEIGHT                                # attachment distance
velocity_at_surface = np.zeros_like(slope_dist)

for i, d in enumerate(slope_dist):
    if d < STANDOFF:
        # Jet is still developing – linear ramp from nozzle to surface
        velocity_at_surface[i] = AIR_VELOCITY * (d / STANDOFF)
    else:
        # Wall-jet decay after attachment
        velocity_at_surface[i] = AIR_VELOCITY * np.sqrt(STANDOFF / d)

velocity_at_surface = np.clip(velocity_at_surface, 0, AIR_VELOCITY)

# ── Drag force on leaves at each point ──
drag_force = 0.5 * RHO_AIR * velocity_at_surface**2 * C_DRAG * LEAF_AREA

# Add a gravity assist component along the slope (small leaf mass)
LEAF_MASS = 0.002  # 2 g wet leaf
gravity_along_slope = LEAF_MASS * 9.81 * np.sin(slope_rad)
total_clearing_force = drag_force + gravity_along_slope

clearing_zone = total_clearing_force > LEAF_STICTION_FORCE

# ══════════════════════════  PLOTTING  ══════════════════════════
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8),
                                gridspec_kw={'height_ratios': [2, 1]})

# ── Plot 1: Physical Layout ──
ax1.set_title("Apex Nozzle: Top-Down Air Blade on Sloped Roof",
              fontsize=14, fontweight='bold')

# Draw roof surface
ax1.plot(x_roof, y_roof, color='#4a4a4a', linewidth=8,
         label="Sloped Roof (Shingle Surface)")

# Draw ground line for reference
ax1.axhline(0, color='#8B4513', linewidth=2, linestyle='-', alpha=0.3)

# Nozzle polygon at apex
nw = 0.012  # nozzle half-width
nozzle_poly = Polygon(
    [[nozzle_x - nw, nozzle_y + 0.03],
     [nozzle_x + nw, nozzle_y + 0.03],
     [nozzle_x + nw/2, nozzle_y],
     [nozzle_x - nw/2, nozzle_y]],
    closed=True, color='silver', ec='black', linewidth=1.5,
    label="Nozzle (at Apex)", zorder=5
)
ax1.add_patch(nozzle_poly)

# Airflow cone from nozzle down along slope
cone_reach = min(0.25, ROOF_LENGTH)  # visual reach of drawn cone
idx_reach = np.argmin(np.abs(slope_dist - cone_reach))
offset = 0.025  # perpendicular spread of drawn cone
nx = np.cos(slope_rad + np.pi/2) * offset
ny = np.sin(slope_rad + np.pi/2) * offset
jet_cone_x = [nozzle_x, x_roof[idx_reach] + nx, x_roof[idx_reach] - nx, nozzle_x]
jet_cone_y = [nozzle_y, y_roof[idx_reach] + ny, y_roof[idx_reach] - ny, nozzle_y]
ax1.fill(jet_cone_x, jet_cone_y, color='cyan', alpha=0.25, label="Airflow Jet")

# Clearing zone highlights on roof
ax1.fill_between(x_roof, y_roof, y_roof + 0.008,
                 where=clearing_zone, color='lime', alpha=0.8,
                 label="Clearing Zone (Leaves Removed)")
ax1.fill_between(x_roof, y_roof, y_roof + 0.008,
                 where=~clearing_zone, color='darkorange', alpha=0.5,
                 label="Stiction > Force (Leaves Remain)")

# Draw example leaves
leaf_positions = [0.05, 0.12, 0.22, 0.35, 0.48, 0.55]
for ld in leaf_positions:
    idx = np.argmin(np.abs(slope_dist - ld))
    lx, ly = x_roof[idx], y_roof[idx]
    if clearing_zone[idx]:
        # Leaf being swept downslope
        ax1.plot(lx + 0.015, ly - 0.01, marker='o', markersize=7,
                 color='green', alpha=0.6)
        ax1.annotate('', xy=(lx + 0.015, ly - 0.01), xytext=(lx, ly + 0.005),
                     arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    else:
        # Leaf stuck on roof
        ax1.plot(lx, ly + 0.005, marker='o', markersize=7, color='darkgreen')

# Annotation for apex
ax1.annotate("APEX\n(nozzle here)", xy=(nozzle_x, nozzle_y),
             xytext=(0.08, nozzle_y + 0.04),
             fontsize=9, fontweight='bold', color='navy',
             arrowprops=dict(arrowstyle='->', color='navy'))

# Gravity arrow
gx, gy = x_roof[len(x_roof)//2], y_roof[len(y_roof)//2] + 0.04
ax1.annotate('gravity\nassist', xy=(gx + 0.03, gy - 0.03), xytext=(gx, gy),
             fontsize=8, color='gray',
             arrowprops=dict(arrowstyle='->', color='gray', lw=1))

ax1.set_xlabel("Horizontal Distance from Apex (m)")
ax1.set_ylabel("Height (m)")
ax1.set_xlim(-0.05, ROOF_LENGTH * np.cos(slope_rad) + 0.05)
ax1.set_ylim(-0.02, apex_height + NOZZLE_HEIGHT + 0.08)
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.set_aspect('equal')

# ── Plot 2: Force Analysis ──
ax2.set_title("Force Analysis Along Roof Slope (from Apex)", fontsize=12)
ax2.plot(slope_dist, drag_force, color='blue', linewidth=2,
         label="Aerodynamic Drag Force")
ax2.plot(slope_dist, total_clearing_force, color='dodgerblue', linewidth=1.5,
         linestyle='-.', label="Total (Drag + Gravity Component)")
ax2.axhline(LEAF_STICTION_FORCE, color='red', linestyle='--', linewidth=2,
            label=f"Wet Leaf Stiction ({LEAF_STICTION_FORCE} N)")

ax2.fill_between(slope_dist, total_clearing_force, LEAF_STICTION_FORCE,
                 where=clearing_zone, color='lime', alpha=0.3)

ax2.set_xlabel("Distance Along Slope from Apex (m)")
ax2.set_ylabel("Force (N)")
ax2.set_xlim(0, ROOF_LENGTH)
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
out_path = "apex_clear_visualization.png"
plt.savefig(out_path, dpi=200)
print(f"Saved visualization to {out_path}")
