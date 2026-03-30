# Changes Already Made & Changes Still Needed

## Changes Already Applied to PrototypeOverview.tex

1. **Deleted Double-Sided Air Blade fake data** from Test 1 force table (row with 1.91/1.88/1.85/1.62). We have a double-sided nozzle but never tested that mode quantitatively. "four nozzle geometries" → "three."
2. **Added all 6 team member names and roles** to Introduction: Memo (fluid dynamics/data), Markiyan (CircuitPython/stepper), Kimmy (specs/verification), Rihanna (CAD/notebook/3D prints), Hannah (test setup/procurement), Karys (CAD/reports/verification).
3. **Fixed GPIO pins** from GP5/GP6 → GP15/GP16 to match real `PraxisCode.py`. Fixed EN/STEP/DIR to GP0/GP1/GP2.
4. **Fixed switch model** from generic "Omron" → D2FS-FL-N (actual part from dossier).
5. **Fixed firmware description** — removed "interrupt-style state machine" claim. Real code is polling loop with 4-cycle auto-stop and dual-button reset. References `PraxisCode.py` instead of fictional `code.py`.
6. **Made dual-nozzle bidirectional design explicit** in architecture table.
7. **Fixed integration change #5** to match real firmware behavior.

---

## Changes Still Needed (for main agent to execute)

### CRITICAL: As-Built Photograph
The rubric STRICTLY requires "A photograph of your Prototype System as-built." There is NO standalone photo in the dossier. Options:
- Extract a frame from `04_Prototype/track videos/Track_Short_Overview.mov` or `Track_Main_Continuous_Cycle.mov`
- The HEIC photos in `04.3_Integration/` show partial assemblies (e.g., `V2RidgeTrackSystem(newAxle&Connection).HEIC`)
- If someone has a photo of the complete system with Pico + hairdryer + track, add it

The placeholder is at line ~100-108 in `PrototypeOverview.tex`. Uncomment and point to the real file.

### CRITICAL: Figure 2 Photo Verification
Previous Justin flagged that `Stepper_A4988_ScrewTerminals_Final.jpeg` might just be another angle of the DC motor, not the actual final A4988 setup. **Check this photo.** If it's wrong, replace with a real photo of Markiyan's final stepper+A4988+screw terminal board. The photo is at line ~173 in the .tex.

Looking at it: the image shows a yellow DC motor AND a black Nema 17 side-by-side from above. It IS the motor comparison shot — it's showing both the OLD (yellow DC) and NEW (Nema 17 stepper) motors together. The caption says "Final: Nema 17 + A4988 + screw terminals" but the photo doesn't show the A4988 or screw terminals at all, just the two motors. **This caption is misleading.** Either:
- Get a real photo of the A4988+screw terminal setup for the "Final" slot
- Or relabel the caption to say "Motor comparison: DC (left) vs. Nema 17 (right)" and restructure Figure 2 as a 2-panel instead of 3-panel

### Photos Available in Dossier (NOT yet linked as figures)
These are in `/Users/memoozdincer/Documents/ESC203/Team0109D_DD2_DesignDossier/04_Prototype/`:

**Integration photos (04.3_Integration/):**
- `V1BrokenPulleyAxle.HEIC` — V1 axle that broke/bent under tension
- `V1vsV2PulleyAxle.HEIC` — Side-by-side axle comparison (already in repo)
- `V2RidgeTrackSystem(newAxle&Connection).HEIC` — V2 assembled system
- `OldTimingBelt.png` — Smooth belt that slipped (already in repo)
- `BeltWithIndentations.HEIC` — New belt with grip indents (already in repo)

**Integration videos (04.3_Integration/) — LINK, don't download:**
- `MotorDrivenNozzleCarriage.mov` — motor driving the nozzle cart
- `StruggleswithMovementTrackwithNozzleCart.mov` — pre-fix struggles
- `FixedStruggleswithMovementTrackwithNozzleCart.MOV` — post-fix success
- `TensionInAxlePulley.mov` — tension issues
- `V2RidgeTrackMovement.MOV` — V2 system moving

**Verification (04.4_Verification/):**
- `ClosureElectrical.png` — electrical closure photo
- `ESC204S_2026_DD2_VerificationProtocol+Results.xlsx` — THE real verification spreadsheet

**Track videos (track videos/):**
- `Track_Main_Continuous_Cycle.mov` / `.mp4` — the 2-minute endurance test
- `Track_Short_Overview.mov` — short demo clip
- `Stopping_at_end_of_cycle.mp4` — limit switch stopping behavior

**Air blade test videos (circular_vs_nozzle/):**
- `circular_distance1_test.mov`, `circular_distance2_test.mov`, `circular_distance3_test.mov`
- `nozzle_distance1_test.mov`, `nozzle_distance2_test.mov`, `nozzle_distance3_test.mov`
- `circular_wet_test.mov`, `nozzle_wet_test.mov`

These 8 videos are THE real verification trials referenced in the document. The Google Drive links in the LaTeX should point to these.

### Downstream File Routing (per Justin's master plan + rubric)

| File | Action | Reason |
|------|--------|--------|
| `04.4_Verification_Summary.tex/.pdf` | **TRASH** | Rubric Section 4.2.4 demands a SPREADSHEET. Submit `ESC204S_2026_DD2_VerificationProtocol+Results.xlsx` instead |
| `05.0_Engineering_Notebook.tex/.pdf` | **TRASH** | AI-generated notebook looks fake. Submit Rihanna's real `Team Engineering Notebook.docx` (already exported as `Team_Engineering_Notebook.pdf`) |
| `04.2_Build_Process.tex/.pdf` | **KEEP & EDIT** | Strip hallucinations, insert real `PraxisCode.py`, add real CAD renders |
| `04.3_Integration_Log.tex/.pdf` | **KEEP & EDIT** | Focus on real failures with real photos (V1BrokenPulleyAxle, OldTimingBelt, etc.) |

### Real Dates from Dossier (for accuracy)
- **March 10:** MYFab mentor confirmed aluminum T-slot approach (Studio 10A)
- **March 11:** Order #1 submitted (two 20cm extrusions)
- **March 13:** Hannah created shared "to print" Google Drive folder; Order #2 (V1 pulleys/axles/belt)
- **March 17:** V1 track tested in Studio 11A — too short (40cm); V1 pulley axles teardrop-shaped, axles bent, belt slipped
- **March 19:** Order #3 (third extrusion for 60cm track, V2 thicker axles + triangle brackets + indented TPU belt)
- **March 25:** Full integration + 2-minute endurance test passed
- **March 26-28:** All verification tests conducted

### Key Facts from Real Dossier That Differ from LaTeX
1. **Original motor was a 3-6V DC gear motor at $2.35** (not a generic "DC motor")
2. **Original air source was a ball pump** (per Updated Team Charter), not an air compressor
3. **Track is 3× 20cm aluminum T-slot extrusions bolted together** (not a single 60cm piece)
4. **The code has NO homing routine** — PraxisCode.py just starts polling immediately. The repo's `firmware/code.py` with homing/serial commands is an idealized version, not what runs on the Pico.
5. **Team name is "StepUp"** (from Team Charter)
6. **Limit switch model: D2FS-FL-N** (already fixed in LaTeX)
