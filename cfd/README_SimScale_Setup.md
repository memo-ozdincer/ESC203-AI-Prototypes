# SimScale CFD Setup Guide — Air Blade Impinging Jet

## Purpose
Generate a velocity vector heat-map showing the Coanda effect (air attaching to the roof surface) and the shear stress applied to the boundary layer. This corroborates the mathematical drag-force calculations and the physical tuft test.

## Step-by-Step Setup

### 1. Create an Account
- Go to [simscale.com](https://www.simscale.com) and sign up for a free Community account.

### 2. Create a New Project
- Click **Create New Project** and name it `ESC203_AirBlade_CFD`.

### 3. Import or Create Geometry
Since SimScale is 3D, create a thin extruded 2D-equivalent domain:

- Use the built-in **CAD modeler** or upload a STEP file.
- **Domain dimensions:**
  - Length (x): 400 mm (along roof surface)
  - Height (y): 150 mm (above surface)
  - Depth (z): 10 mm (thin slab for pseudo-2D)
- **Nozzle slit:** A 3 mm wide opening positioned 50 mm above the surface, angled at 30° to the surface.
- The bottom face represents the roof surface (wall boundary).

### 4. Set Up the Simulation
- **Analysis type:** Incompressible (subsonic airflow)
- **Turbulence model:** k-omega SST (good for wall-bounded jets and separation)
- **Material:** Air at 20°C (rho = 1.204 kg/m³, mu = 1.825e-5 Pa·s)

### 5. Boundary Conditions

| Boundary       | Type               | Value                    |
|----------------|--------------------|--------------------------|
| Nozzle inlet   | Velocity inlet     | 20 m/s normal to face    |
| Domain outlet  | Pressure outlet    | 0 Pa gauge               |
| Roof surface   | No-slip wall       | —                        |
| Top boundary   | Slip wall          | —                        |
| Front/back     | Symmetry           | — (enforces 2D behavior) |

### 6. Mesh Settings
- Use **automatic meshing** with the following refinements:
  - **Surface refinement** on the roof wall: minimum cell size 0.5 mm (captures boundary layer).
  - **Region refinement** around the nozzle exit: minimum cell size 0.3 mm.
  - **Boundary layer mesh** on the roof surface: 8 layers, expansion ratio 1.2, first layer thickness 0.05 mm.
- Target total cell count: 200k–500k (within free-tier limits).

### 7. Run the Simulation
- Set **end time** to 500 iterations (steady-state solver).
- Click **Start Simulation** and wait for convergence (residuals below 1e-4).

### 8. Post-Processing
In the SimScale online post-processor:

1. **Velocity magnitude contour:** Select a mid-plane slice (z = 5 mm). Apply a colour map (e.g., "jet" or "coolwarm"). This shows the high-velocity core of the air blade and how it attaches to the surface (Coanda effect).
2. **Velocity vectors:** Overlay vectors on the same slice to show flow direction, especially the turning of the jet toward the wall.
3. **Wall shear stress:** Plot wall shear stress on the roof surface. The peak shear zone is where leaf removal force is greatest.
4. **Export screenshots** for the final report.

## Key Results to Look For
- The jet should visibly **curve toward and attach to the roof surface** after impingement (Coanda effect).
- **Wall shear stress** should peak near the impingement point and remain elevated downstream — this is the mechanism that overcomes wet leaf stiction.
- Compare the peak shear stress to the stiction force from `analysis/drag_force_calculation.py` to confirm the air blade produces sufficient force.

## Tips
- If the jet separates from the wall, try reducing the nozzle angle (e.g., 15°) or increasing velocity.
- For a quick qualitative check, run at coarser mesh first (~100k cells), then refine.
- Screenshots from SimScale can be directly embedded in the ESC203 report as CFD evidence.
