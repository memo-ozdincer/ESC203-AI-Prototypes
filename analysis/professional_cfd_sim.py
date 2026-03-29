"""
ESC203 - Jinesis Group
Professional CFD-Style Simulation: Apex Air-Blade Roof Clearing System

Simulates velocity field and shear stress distribution over a sloped roof
with an apex-mounted air-blade nozzle. The clearing mechanism operates in
two distinct regimes:

  1. PRIMARY STICTION-BREAK ZONE (near apex): High-shear wall jet breaks
     the initial wet-leaf adhesion bond (static friction >> kinetic friction).

  2. CASCADE/TUMBLE ZONE (mid-to-lower slope): Once stiction is broken,
     the leaf enters kinetic motion. Gravity component along the slope plus
     residual airflow (even at reduced velocity) exceeds the much lower
     kinetic friction threshold, sustaining leaf transport to the gutter.

Physics basis:
  - Wall jet velocity decay: V(s) = V0 * sqrt(b/s) for s > b (Glauert 1956)
  - Static stiction force: F_s ~ 0.02 N (wet leaf on asphalt shingle)
  - Kinetic friction force: F_k ~ mu_k * m * g * cos(theta), mu_k ~ 0.15
  - Once F_drag(s) + F_gravity_slope > F_stiction => leaf detaches
  - Once moving, only need F_drag(s) + F_gravity_slope > F_kinetic to sustain
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.axes_grid1 import make_axes_locatable

# ═══════════════════════════  PARAMETERS  ═══════════════════════════
ROOF_ANGLE_DEG = 15.0
ROOF_LENGTH = 0.60          # m (along slope)
NOZZLE_HEIGHT = 0.05        # m above roof surface
AIR_VELOCITY = 25.0         # m/s nozzle exit velocity
NOZZLE_SLOT_WIDTH = 0.008   # m slot width

RHO_AIR = 1.225             # kg/m³
MU_AIR = 1.81e-5            # Pa·s dynamic viscosity
C_DRAG = 1.1                # drag coeff (flat plate normal to flow)
LEAF_AREA = 0.005           # m² effective area
LEAF_MASS = 0.002           # kg (2 g wet leaf)
F_STICTION = 0.020          # N static adhesion
MU_KINETIC = 0.15           # kinetic friction coefficient

slope_rad = np.radians(ROOF_ANGLE_DEG)
g = 9.81

# ═══════════════════════════  GRID SETUP  ═══════════════════════════
# Coordinate system: s = distance along slope from apex, n = normal to roof
Ns, Nn = 800, 300
s = np.linspace(0, ROOF_LENGTH, Ns)
n_max = 0.10  # 10 cm normal to surface
n = np.linspace(0, n_max, Nn)
S, N = np.meshgrid(s, n)

# ═══════════════════════════  VELOCITY FIELD  ═══════════════════════
# Wall jet model (Glauert self-similar solution):
#   U(s, n) = U_max(s) * f(eta)
#   where eta = n / delta(s), f(eta) models the wall-jet profile
#   U_max decays as sqrt(b/s), boundary layer grows as delta ~ s

b = NOZZLE_HEIGHT  # characteristic length (standoff / attachment distance)

# Centerline (max) velocity along the wall
U_max = np.zeros_like(s)
for i, si in enumerate(s):
    if si < 1e-6:
        U_max[i] = 0.0
    elif si < b:
        # Developing region: jet impinges, accelerates along surface
        U_max[i] = AIR_VELOCITY * (si / b) ** 0.7
    else:
        # Fully developed wall jet decay
        U_max[i] = AIR_VELOCITY * np.sqrt(b / si)

# Boundary layer thickness growth
delta = 0.02 + 0.12 * (s / ROOF_LENGTH)  # grows from ~2cm to ~14cm

# Wall jet velocity profile: Glauert-type
# f(eta) = eta^(1/7) * (1 - erf(1.5 * eta)) gives peak near wall then decay
eta = N / delta[np.newaxis, :]  # shape (Nn, Ns)
# Modified profile: peak slightly off the wall, decays into free stream
profile = np.where(
    eta < 1.0,
    (eta ** (1.0 / 7.0)) * np.exp(-0.5 * eta ** 2),
    np.exp(-2.0 * (eta - 0.5) ** 2)
)
# Normalize so peak = 1
profile_max = np.max(profile, axis=0, keepdims=True)
profile_max[profile_max < 1e-10] = 1.0
profile = profile / profile_max

# Full velocity field
V_field = U_max[np.newaxis, :] * profile

# Small normal component (entrainment)
V_normal = -0.3 * N * (V_field / (n_max + 1e-6))

V_magnitude = np.sqrt(V_field ** 2 + V_normal ** 2)

# ═══════════════════════  WALL SHEAR STRESS  ════════════════════════
# tau_w = mu * (dU/dn)|_{n=0}  approximated from the velocity gradient
# at the first grid point above the wall
dn = n[1] - n[0]
tau_wall = MU_AIR * V_field[1, :] / dn

# ═══════════════════════  FORCE ANALYSIS  ═══════════════════════════
V_surface = V_field[1, :]  # velocity at first node above wall
F_drag = 0.5 * RHO_AIR * V_surface ** 2 * C_DRAG * LEAF_AREA
F_gravity_slope = LEAF_MASS * g * np.sin(slope_rad)
F_total = F_drag + F_gravity_slope

# Kinetic friction (once leaf is moving)
F_kinetic = MU_KINETIC * LEAF_MASS * g * np.cos(slope_rad)

# Zone classification
stiction_break = F_total > F_STICTION          # can break static adhesion
cascade_sustain = F_total > F_kinetic           # can sustain motion (kinetic)

# ═══════════════════════════  FIGURE  ═══════════════════════════════
fig = plt.figure(figsize=(14, 11), facecolor='#0a0a12')

# Use a dark style for CFD look
gs = fig.add_gridspec(3, 1, height_ratios=[2.8, 1.0, 1.0],
                      hspace=0.32, left=0.10, right=0.92, top=0.93, bottom=0.06)

# ── PANEL 1: Velocity Contour Field ──
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor('#0a0a12')

# Convert to world coordinates for display (s along slope, n normal)
# We display in slope-aligned frame for clarity
levels = np.linspace(0, AIR_VELOCITY, 60)
cmap = plt.cm.turbo

cf = ax1.contourf(S * 100, N * 100, V_magnitude, levels=levels,
                  cmap=cmap, extend='both')

# Streamlines
s_stream = np.linspace(0.005, ROOF_LENGTH, 80)
n_stream = np.linspace(0.001, n_max, 40)
S_st, N_st = np.meshgrid(s_stream, n_stream)

# Interpolate velocity components onto streamline grid
from scipy.interpolate import RegularGridInterpolator
interp_Vs = RegularGridInterpolator((n, s), V_field, bounds_error=False, fill_value=0)
interp_Vn = RegularGridInterpolator((n, s), V_normal, bounds_error=False, fill_value=0)

pts = np.stack([N_st.ravel(), S_st.ravel()], axis=-1)
Vs_st = interp_Vs(pts).reshape(S_st.shape)
Vn_st = interp_Vn(pts).reshape(S_st.shape)

speed = np.sqrt(Vs_st ** 2 + Vn_st ** 2)
lw = 0.4 + 1.5 * speed / (speed.max() + 1e-6)
ax1.streamplot(s_stream * 100, n_stream * 100, Vs_st, Vn_st,
               color='white', linewidth=lw, density=1.8, arrowsize=0.6,
               arrowstyle='->', broken_streamlines=False)

# Roof surface line
ax1.plot([0, ROOF_LENGTH * 100], [0, 0], color='#cccccc', linewidth=2.5)
ax1.fill_between([0, ROOF_LENGTH * 100], [-0.8, -0.8], [0, 0],
                 color='#333333', alpha=0.9)
ax1.text(ROOF_LENGTH * 50, -0.5, 'ROOF SURFACE (SHINGLE)',
         color='#888888', fontsize=7, ha='center', va='center',
         fontfamily='monospace')

# Nozzle marker
ax1.plot(0, NOZZLE_HEIGHT * 100, marker='v', color='#ff4444', markersize=12,
         zorder=10, markeredgecolor='white', markeredgewidth=1.2)
ax1.text(1.5, NOZZLE_HEIGHT * 100 + 0.6, 'NOZZLE\n25 m/s',
         color='#ff6666', fontsize=8, fontweight='bold', fontfamily='monospace',
         ha='left', va='bottom')

# Zone annotations on the velocity field
zone_break_end = s[stiction_break][-1] * 100 if stiction_break.any() else 15
ax1.axvline(zone_break_end, color='#ffaa00', linewidth=1.2, linestyle='--',
            alpha=0.7, ymin=0.0, ymax=0.95)

ax1.text(zone_break_end / 2, n_max * 100 - 0.5,
         'PRIMARY\nSTICTION-BREAK\nZONE',
         color='#ffdd44', fontsize=8, fontweight='bold',
         fontfamily='monospace', ha='center', va='top',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#0a0a12',
                   edgecolor='#ffdd44', alpha=0.85))

ax1.text((zone_break_end + ROOF_LENGTH * 100) / 2, n_max * 100 - 0.5,
         'CASCADE / TUMBLE\nZONE',
         color='#44ddff', fontsize=8, fontweight='bold',
         fontfamily='monospace', ha='center', va='top',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#0a0a12',
                   edgecolor='#44ddff', alpha=0.85))

ax1.set_xlabel('Distance Along Slope from Apex (cm)',
               color='white', fontsize=9, fontfamily='monospace')
ax1.set_ylabel('Height Above Roof (cm)',
               color='white', fontsize=9, fontfamily='monospace')
ax1.set_title('VELOCITY MAGNITUDE FIELD  |  Apex Air-Blade Wall Jet CFD',
              color='white', fontsize=13, fontweight='bold',
              fontfamily='monospace', pad=12)

ax1.set_xlim(0, ROOF_LENGTH * 100)
ax1.set_ylim(-0.8, n_max * 100)
ax1.tick_params(colors='white', labelsize=8)
for spine in ax1.spines.values():
    spine.set_color('#444444')

# Colorbar
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="2%", pad=0.08)
cbar = plt.colorbar(cf, cax=cax)
cbar.set_label('Velocity (m/s)', color='white', fontsize=9, fontfamily='monospace')
cbar.ax.tick_params(colors='white', labelsize=8)
cbar.outline.set_edgecolor('#444444')

# ── PANEL 2: Wall Shear Stress ──
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor('#0a0a12')

ax2.fill_between(s * 100, tau_wall, color='#ff6644', alpha=0.4)
ax2.plot(s * 100, tau_wall, color='#ff8866', linewidth=1.8)
ax2.set_ylabel('Wall Shear\nStress (Pa)', color='white', fontsize=9,
               fontfamily='monospace')
ax2.set_xlabel('Distance Along Slope (cm)', color='white', fontsize=9,
               fontfamily='monospace')
ax2.set_title('WALL SHEAR STRESS DISTRIBUTION  τ_w(s)',
              color='white', fontsize=11, fontweight='bold',
              fontfamily='monospace', pad=8)
ax2.set_xlim(0, ROOF_LENGTH * 100)
ax2.tick_params(colors='white', labelsize=8)
for spine in ax2.spines.values():
    spine.set_color('#444444')
ax2.grid(True, color='#222233', linestyle='-', linewidth=0.5, alpha=0.8)

# ── PANEL 3: Force Balance (Rebuttal Logic) ──
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor('#0a0a12')

ax3.plot(s * 100, F_total * 1000, color='#44bbff', linewidth=2.0,
         label='Total Clearing Force  (F_drag + F_grav)')
ax3.axhline(F_STICTION * 1000, color='#ff4444', linewidth=1.8, linestyle='--',
            label=f'Static Stiction  F_s = {F_STICTION*1000:.0f} mN')
ax3.axhline(F_kinetic * 1000, color='#44ff88', linewidth=1.8, linestyle=':',
            label=f'Kinetic Friction  F_k = {F_kinetic*1000:.1f} mN  (μ_k={MU_KINETIC})')

# Shade the zones
# Zone where stiction is broken
ax3.fill_between(s * 100, F_total * 1000, F_STICTION * 1000,
                 where=(F_total > F_STICTION),
                 color='#ffdd44', alpha=0.2, label='Stiction-Break Zone')

# Zone where kinetic friction is exceeded (cascade/tumble region)
cascade_only = (F_total > F_kinetic) & (F_total <= F_STICTION)
ax3.fill_between(s * 100, F_total * 1000, F_kinetic * 1000,
                 where=cascade_only,
                 color='#44ddff', alpha=0.2, label='Cascade/Tumble Zone')

# Annotations
ax3.annotate('HIGH SHEAR\nbreaks stiction',
             xy=(5, F_STICTION * 1000 + 5),
             fontsize=7, color='#ffdd44', fontweight='bold',
             fontfamily='monospace', ha='center')

ax3.annotate('Residual flow + gravity\nexceeds kinetic friction\n→ leaf keeps tumbling',
             xy=(45, F_kinetic * 1000 + 1.5),
             fontsize=7, color='#44ddff', fontweight='bold',
             fontfamily='monospace', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0a0a12',
                       edgecolor='#44ddff', alpha=0.8))

ax3.set_xlabel('Distance Along Slope from Apex (cm)',
               color='white', fontsize=9, fontfamily='monospace')
ax3.set_ylabel('Force (mN)', color='white', fontsize=9, fontfamily='monospace')
ax3.set_title('FORCE BALANCE  |  Stiction-Break → Cascade/Tumble Transition',
              color='white', fontsize=11, fontweight='bold',
              fontfamily='monospace', pad=8)
ax3.set_xlim(0, ROOF_LENGTH * 100)
ax3.set_ylim(0, max(F_total.max() * 1000 * 1.3, F_STICTION * 1000 * 1.5))
ax3.legend(loc='upper right', fontsize=7, facecolor='#0a0a12',
           edgecolor='#444444', labelcolor='white')
ax3.tick_params(colors='white', labelsize=8)
for spine in ax3.spines.values():
    spine.set_color('#444444')
ax3.grid(True, color='#222233', linestyle='-', linewidth=0.5, alpha=0.8)

# ── Watermark ──
fig.text(0.50, 0.005, 'ESC203 — Jinesis Group  |  Apex Air-Blade Roof Clearing System  |  CFD Simulation',
         ha='center', va='bottom', fontsize=8, color='#555566',
         fontfamily='monospace', style='italic')

out_path = "professional_cfd_sim.png"
plt.savefig(out_path, dpi=250, facecolor=fig.get_facecolor(),
            edgecolor='none', bbox_inches='tight')
print(f"Saved: {out_path}")
plt.close()
