"""
ESC203 - Jinesis Group
Theoretical Shear Layer & Velocity Field Visualization

Simulates a 2D air blade jet impinging on a flat surface at an angle,
showing the velocity magnitude field and the wall-parallel shear stress
that drives wet leaf removal. Uses a simplified analytical model
(planar free jet + image method for wall interaction).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# ----- Parameters -----
V_JET = 20.0          # m/s  nozzle exit velocity
NOZZLE_WIDTH = 0.003  # m    slit nozzle width (3 mm)
JET_ANGLE_DEG = 30.0  # degrees from the surface
STANDOFF = 0.05       # m    nozzle-to-surface distance
RHO = 1.225           # kg/m^3
MU = 1.81e-5          # Pa·s  dynamic viscosity of air

# Grid
NX, NY = 300, 150
X_RANGE = (-0.05, 0.25)  # metres along the surface
Y_RANGE = (0.0, 0.10)    # metres above the surface

x = np.linspace(*X_RANGE, NX)
y = np.linspace(*Y_RANGE, NY)
X, Y = np.meshgrid(x, y)

# ----- Jet model -----
# The nozzle is positioned at the point where the jet centreline
# would meet the surface (x=0, y=0) and the jet propagates at
# JET_ANGLE from the surface.
theta = np.radians(JET_ANGLE_DEG)

# Coordinate along the jet axis (s) and perpendicular to it (n)
# Origin at impingement point; jet source is at negative s.
S = X * np.cos(theta) + Y * np.sin(theta)
N = -X * np.sin(theta) + Y * np.cos(theta)

# Distance from nozzle exit along centreline
s_nozzle = -STANDOFF  # nozzle is upstream
s_from_nozzle = S - s_nozzle
s_from_nozzle = np.clip(s_from_nozzle, 0.001, None)

# Gaussian spreading: half-width grows as b(s) = 0.1 * s (typical free jet)
SPREAD_RATE = 0.10
b = SPREAD_RATE * s_from_nozzle + NOZZLE_WIDTH / 2

# Centreline velocity decays as 1/sqrt(s) for a 2-D planar jet
s_ref = STANDOFF  # reference distance (nozzle-to-surface)
V_centre = V_JET * np.sqrt(s_ref / s_from_nozzle)
V_centre = np.clip(V_centre, 0, V_JET)

# Gaussian velocity profile across the jet width
V_mag = V_centre * np.exp(-0.5 * (N / b) ** 2)

# Mask the region "behind" the nozzle (upstream of exit)
behind_nozzle = S < s_nozzle
V_mag[behind_nozzle] = 0.0

# Velocity components (for quiver arrows)
Vx = V_mag * np.cos(theta)
Vy = V_mag * np.sin(theta)

# Near the wall (Coanda turn): redirect flow to be wall-parallel
# Simple blending: within one jet-width of the surface, rotate velocity
wall_blend = np.clip(1.0 - Y / (2 * NOZZLE_WIDTH + 0.005), 0, 1)
Vx_wall = V_mag  # fully horizontal at wall
Vy_wall = 0.0
Vx = Vx * (1 - wall_blend) + Vx_wall * wall_blend
Vy = Vy * (1 - wall_blend)
V_total = np.sqrt(Vx**2 + Vy**2)

# Wall shear stress estimate: tau_w ~ mu * du/dy at y=0
# From the velocity field, approximate du/dy at the first cell above y=0
dy = y[1] - y[0]
tau_wall = MU * V_total[0, :] / dy  # simplified

# ----- Plotting -----
fig, axes = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={"height_ratios": [3, 1]})

# Top: velocity magnitude heat map + streamlines
ax1 = axes[0]
norm = Normalize(vmin=0, vmax=V_JET)
cf = ax1.contourf(X * 100, Y * 100, V_total, levels=60, cmap="inferno", norm=norm)
cbar = fig.colorbar(cf, ax=ax1, label="Velocity magnitude (m/s)")

# Quiver (subsample)
skip = 8
ax1.quiver(
    X[::skip, ::skip] * 100,
    Y[::skip, ::skip] * 100,
    Vx[::skip, ::skip],
    Vy[::skip, ::skip],
    color="white",
    alpha=0.6,
    scale=200,
)

# Nozzle position indicator
nozzle_x = -STANDOFF * np.cos(theta) * 100
nozzle_y = STANDOFF * np.sin(theta) * 100
ax1.annotate(
    "Nozzle",
    xy=(nozzle_x, nozzle_y),
    fontsize=10,
    color="cyan",
    fontweight="bold",
    ha="center",
)
ax1.plot([nozzle_x, 0], [nozzle_y, 0], "c--", linewidth=1.5, label="Jet centreline")

ax1.set_xlabel("x (cm) — along roof surface")
ax1.set_ylabel("y (cm) — above surface")
ax1.set_title("Air Blade: Theoretical Velocity Field (30° Impinging Jet)")
ax1.set_xlim([X_RANGE[0] * 100, X_RANGE[1] * 100])
ax1.set_ylim([Y_RANGE[0] * 100, Y_RANGE[1] * 100])
ax1.legend(loc="upper right")

# Bottom: wall shear stress
ax2 = axes[1]
ax2.fill_between(x * 100, tau_wall * 1000, alpha=0.4, color="orangered")
ax2.plot(x * 100, tau_wall * 1000, color="orangered", linewidth=2)
ax2.axhline(0, color="gray", linewidth=0.5)
ax2.set_xlabel("x (cm) — along roof surface")
ax2.set_ylabel("Wall shear stress (mPa)")
ax2.set_title("Estimated Wall Shear Stress (drives leaf removal)")
ax2.set_xlim([X_RANGE[0] * 100, X_RANGE[1] * 100])

plt.tight_layout()
plt.savefig("shear_layer_visualization.png", dpi=150)
#plt.show()
print("Saved: shear_layer_visualization.png")
