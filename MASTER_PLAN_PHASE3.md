# Phase 3 Dossier Master Plan (ESC204)

This document contains the exact routing, artifact linking, and text changes required to align the AI-generated LaTeX files with the hard evidence and the ESC204 rubric. 

## 1. Artifacts Downloaded & Linked
I have downloaded the following physical artifacts into `/home/memo/Documents/ESC203/dossier_artifacts/` so the main agent has direct access:
- `Stepper_A4988_ScrewTerminals_Final.jpeg`
- `HBridge_Motor_Iteration2.jpeg`
- `V1vsV2PulleyAxle.HEIC`
- `OldTimingBelt.png`
- `BeltWithIndentations.HEIC`
- `PraxisCode.py`
- `ESC204S_2026_DD2_Specification.xlsx`
- `Team_Engineering_Notebook.pdf`

**Video Links to Inject (DO NOT DOWNLOAD, JUST LINK):**
- `circular_wet_test.mov`, `nozzle_wet_test.mov` (and distance variations)
- `Stopping_at_end_of_cycle.mp4`, `Track_Short_Overview.mov`, `Track_Main_Continuous_Cycle.mov`
- `StruggleswithMovementTrackwithNozzleCart.mov`, `MotorDrivenNozzleCarriage.mov`, `TensionInAxlePulley.mov`

## 2. LaTeX File Routing & Trashing
Based on rubric strictness, we must reroute the downstream files:
*   **TRASH `04.4_Verification_Summary.tex`**: The rubric (Sec 4.2.4) demands a spreadsheet. We submit Kimmy's Excel sheet (`ESC204S_2026_DD2_Specification.xlsx`) instead.
*   **TRASH `05.0_Engineering_Notebook.tex`**: An AI-generated LaTeX notebook looks fabricated. We will submit the authentic Google Doc export (`Team_Engineering_Notebook.pdf`) and Miro PDFs.
*   **KEEP & EDIT `04.2_Build_Process.tex`**: Strip hallucinations. Insert Markiyan's raw `PraxisCode.py` text here, alongside CAD renders of the pulleys and 3D printer settings.
*   **KEEP & EDIT `04.3_Integration_Log.tex`**: Focus entirely on failures. Inject `HBridge_Motor_Iteration2.jpeg` to show the stalled L298N before the A4988 pivot. Include the narrative on power segregation and the 2cm limit-switch deadzone.

## 3. `PrototypeOverview.tex` Edits
This is the priority document. Make the following changes immediately:

**A. Team Process & Recognition**
- The rubric explicitly requires illustrating the "Team Process." Inject the names and roles:
  - **Memo**: Fluid Dynamics / Data
  - **Markiyan**: CircuitPython / Stepper logic
  - **Kimmy**: Specs Matrix & Subsystems
  - **Rihanna**: CAD & Engineering Notebook
  - **Hannah**: Test setup / hosting at Church st

**B. The "Triple Photo" Hallucination**
- Locate Figure 2. Replace the old DC motor placeholder with the real photo of Markiyan's A4988 breadboard/terminal setup (`Stepper_A4988_ScrewTerminals_Final.jpeg`).

**C. The Double-Sided Air Blade Verification**
- **Test 1 Table**: Delete the row containing fake data (e.g., 1.91 & 1.88) for the "Double-Sided Air Blade." We did not test the double-sided functionality. Change the label to "Custom Air Blade" and only include real data comparing it against the baseline Dyson and OEM blade.
- **Architecture Section**: Explicitly mention that the physical build IS a double-sided / dual-nozzle carriage. This proves bidirectional clearing intent, even if the quantitative test focused on planar shear.

**D. Missing As-Built Photo**
- Ensure a wide-shot photograph of the full 60cm track, Pico, and hairdryer is placed on Page 1 to satisfy the strict "Prototype System as-built" rubric requirement. (Pull a frame from `Track_Short_Overview.mov` if a standalone photo isn't available).

**E. Evidence Hyperlinking**
Hyperlink every claim to hard evidence:
- Mechanical: Link CAD screenshots of v1 (teardrop) vs v2 (thick axle) pulleys.
- Mechanical: Link photos showing the smooth TPU belt failing vs the indented TPU belt gripping (`BeltWithIndentations.HEIC`).
- Electrical: Link directly to `PraxisCode.py` showing interrupt-style limit switch logic.
- Electrical: Link to the L298N H-Bridge jitter video.
- Verification: Link the digital kitchen scale photo showing ~200g (1.96N) for Test 1.
- Verification: Link the screenshot of the $30^\circ$ vector decomposition math next to the Wet Stiction video links.
- Process: Link Kimmy's Excel specification sheet in Section 6.
- Process: Link Rihanna's Engineering Notebook.
