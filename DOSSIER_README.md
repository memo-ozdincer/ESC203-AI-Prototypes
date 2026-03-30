# Dossier Artifacts Generated — March 29, 2026

This README documents all artifacts generated in this session for the ESC204 Design Dossier Submission #2 (due March 30, 2026 at 11:59 AM). A follow-up agent with additional project context will link more artifacts and cross-check against the full dossier folder structure.

## IMPORTANT: Quality & Trust Levels

**The Prototype Overview (`PrototypeOverview.tex/.pdf`) is the only thoroughly vetted document.** It was carefully constructed from extensive source material (LaTeX verification docs, firmware code, test data CSVs, rubric requirements, team notes, and the pulley iteration PDF). It went through multiple revision passes to fit 5 pages and hit every rubric checkbox. **This is submission-ready** (pending the as-built photo).

**Everything else in `dossier_artifacts/` is a naive first-pass draft.** These documents (Build Process, Integration Log, Verification Summary, Engineering Notebook) were generated rapidly to give the team a starting skeleton. They should be treated as **templates to cherry-pick from, NOT as finished artifacts**. Specifically:
- **Dates, team member names, and some procedural details are fabricated/estimated** — they need to be verified against actual team records
- **The Engineering Notebook entries are entirely synthetic** — the structure and format are rubric-appropriate, but the content must be checked against what actually happened and when
- **Technical content is generally accurate** (pulled from the same source material as the Prototype Overview), but phrasing and emphasis may not match what the team actually experienced
- **The Build Process and Integration Log** contain reliable technical facts (pin maps, motor specs, iteration history) but the narrative framing is a best guess

**Recommended approach for the next agent:** Use the Prototype Overview as the authoritative source of truth. Pull specific tables, data, and technical descriptions from the dossier artifacts as needed, but rewrite the narrative portions to match the team's actual experience and records.

---

## What Was Generated

### Main Deliverable: Prototype Overview (5 pages)
- **File:** `PrototypeOverview.tex` / `PrototypeOverview.pdf` (in repo root)
- **Goes in:** `04_Prototype/` folder in the SharePoint Design Dossier
- **Filename for submission:** `0109D_DD2_PrototypeOverview.pdf`
- **Format:** Helvetica 12pt, 0.5" margins, 5 pages exactly
- **Contents:**
  1. Introduction
  2. High-Level System Description + prototype layout visualization (Figure 1)
  3. System Architecture table (Design Concept → Prototype mapping, Table 1)
  4. Key Design Decisions:
     - 4.1 Motor & Driver Evolution (3 iteration photos side-by-side, Figure 2)
     - 4.2 Pulley System Iterations (V1/V2 comparison table, Table 2)
     - 4.3 Power Segregation & Thermal Tuning
     - 4.4 Firmware: Delays → Reactive State Machine
  5. Prototype Design Process:
     - 5.1 Integration Changes (6 numbered items)
     - 5.2 Verification (Tests 1-3 + Endurance, Tables 3-4)
  6. Performance vs Specification (all 11 specs PASSED, Table 5)
  7. Challenges Faced (6 items)
  8. Contribution to Design Concept Understanding

### Supporting Dossier Artifacts (in `dossier_artifacts/`)

| File | Pages | Target Dossier Folder | Description |
|------|-------|-----------------------|-------------|
| `04.2_Build_Process.tex/.pdf` | 2 | `04.2_Build` | Electrical iterations table + 3 photos, wiring pin map from `code.py`, pulley V1/V2 table, `single_step()` code snippet, fabrication methods table |
| `04.3_Integration_Log.tex/.pdf` | 2 | `04.3_Integration` | Chronological timeline table, 6 detailed integration changes, 3 iteration photos, video links for jitter failure + endurance test |
| `04.4_Verification_Summary.tex/.pdf` | 3 | `04.4_Verification` | Full 3-test protocol (force data table, clearing comparison, wet stiction PASS/FAIL), CFD shear-layer figure, endurance results, 11-spec compliance table |
| `05.0_Engineering_Notebook.tex/.pdf` | 4 | `05.0_EngineeringNotebook` | 7 dated work log entries (Mar 2–29), team presence, key decisions, artifacts created per entry |

---

## What Still Needs Manual Attention

### 1. As-Built Photograph
The Prototype Overview has a **commented-out placeholder** (around line 68 in the `.tex`) for the required as-built photo. Uncomment and replace the filename:
```latex
% \includegraphics[width=0.55\textwidth]{assembled_prototype_photo.jpeg}
```

### 2. Team Member Names
The Engineering Notebook uses placeholder names: `Memooz, Angela, Liam, Priya, Jaden`. Update to actual team member names.

### 3. Nozzle Design Iterations
Intentionally left blank per instruction — "that's going to be very research based, and a lot of iterations." Add when ready.

### 4. Buy vs. Build Decisions
Intentionally excluded per instruction — those go in `04.1_PrototypeDesign` or `04.2_Build` depending on when the decision was made (before vs. during construction), NOT in the Prototype Overview or Integration.

---

## Existing Repo Structure (Pre-Existing, Not Generated)

These files were already in the repo and were used as source material:

```
images/
  DC_Motor_Breadboard_Iteration1.jpeg   # Circuit Iteration 1 photo
  HBridge_Motor_Iteration2.jpeg         # Circuit Iteration 2 photo (DC vs stepper)
  Stepper_A4988_ScrewTerminals_Final.jpeg  # Final architecture photo
  professional_cfd_sim.png              # CFD velocity magnitude field
  shear_layer_visualization.png         # Theoretical 30° impinging jet model
  prototype_clear_visualization.png     # System layout + force analysis
  apex_clear_visualization.png          # Apex nozzle visualization

firmware/
  code.py                              # CircuitPython for Pico (stepper control)

analysis/
  drag_force_calculation.py            # Drag force math
  shear_layer_visualization.py         # Shear layer viz script
  professional_cfd_sim.py              # CFD simulation script
  apex_nozzle_visualization.py         # Apex viz script
  leaf_clearing_animation.py           # Animation script
  *.png                                # Output visualizations

data/
  force_magnitude_test.tex/.pdf        # Test 1 raw data + analysis
  fluid_dynamics_verification.tex/.pdf # Tests 2-3 raw data + analysis

master_verification_document.tex/.pdf  # Full verification dossier (LaTeX source)
air_blade_testing_protocol.tex/.pdf    # Testing protocol document

MASTER_DOCUMENTATION.md                # Master file linking all images + context
Prototype Overview.txt                 # Original draft (plain text, superseded by .tex)
prototyping_extra/                     # Additional context notes (morecontext.txt, test2and3.txt)
rubrics/                               # Official ESC204 rubrics and handouts
```

---

## Video Artifacts (Google Drive Links)

These are embedded as hyperlinks throughout the generated documents:

| Video | Link |
|-------|------|
| Custom Nozzle Wet Test (SUCCESS) | https://drive.google.com/file/d/16htpF3ptwKEM5UxYE679x3f3xWmt80h1/view |
| Circular Nozzle Wet Test (FAILED) | https://drive.google.com/file/d/1wO-Wh8iFGygEvBvc3OOH91XQSwhoY_Ws/view |
| Track Automation / Endurance Test | https://drive.google.com/drive/folders/1wNK_jYUvHXoMne_cIdYbAIURdvYpuG-J |
| All 8 Air Blade Trial Videos | https://drive.google.com/drive/folders/1RAJA95EF-XjMrkhjWkuoIBbONH_DbRVu |

---

## Specification IDs Referenced

All 11 specs from the Verification Protocol + Results spreadsheet:

| ID | Subsystem | Statement | Status |
|----|-----------|-----------|--------|
| O-1.1-ELEC-1 | Electrical | Traverse full track ≥2 passes | PASS |
| O-2.1-ELEC-1 | Electrical | Activated without roof access | PASS |
| O-2.2-ELEC-1 | Electrical | Insulated electrical components | PASS |
| O-3.2-ELEC-1 | Electrical | Limit switches for direction/energy | PASS |
| O-1.1-STRU-1 | Structural | Sufficient force to dislodge debris | PASS (Test) |
| O-1.1-STRU-2 | Structural | Full-width air coverage | PASS (Test) |
| O-4.1-STRU-1 | Structural | Low-profile, follows roof contour | PASS |
| O-4.2-STRU-1 | Structural | No shingle damage | PASS |
| O-1.3-SOFT-1 | Software | Autonomous 2-pass CLEARING state | PASS |
| O-2.1-SOFT-1 | Software | Ground-level CLEARING activation | PASS |
| O-3.2-SOFT-1 | Software | OFF state: all motors inactive | PASS |

---

## Key Data Points (for cross-referencing)

- **Track:** 60 cm aluminum T-slot, 56 cm active travel between limit switches
- **Motor:** Nema 17, 200 steps/rev, 0.2 mm/step, GT2 belt + 20-tooth pulley = 40 mm/rev
- **Speed:** 56 cm in 22 s = ~2.55 cm/s
- **Force:** ~1.96 N (200 g) conserved across nozzle geometries within 12 cm
- **Angle:** 30° angle of attack (Fy boundary attachment + Fx shear, Coanda effect)
- **Endurance:** 2-minute continuous cycle, zero stalling
- **Power:** Isolated 5V USB (logic) + 12V DC adapter (motor)
- **Thermal:** A4988 VREF tuned to ~50%
- **Test surface:** 35×15 cm mock-up, 40-grit aluminum oxide sandpaper
- **Firmware:** CircuitPython on Raspberry Pi Pico, reactive state machine polling GP5/GP6

---

## Downloaded Files (used as source, in ~/Downloads/)

- `List of Changes During Integration.pdf` — pulley system iteration photos (V1/V2 with red/blue borders)
- `ESC204S_2026_DD2_VerificationProtocol+Results.xlsx - VerificationProtocol+Results.csv` — verification spreadsheet
- `ESC204S_2026_DD2_Specification.xlsx - VerificationProtocol+Results.csv` — specification spreadsheet
