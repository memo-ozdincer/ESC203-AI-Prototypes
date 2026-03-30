# Justin's Rewrite Plan: Section 4 & Justifications 🎤

Baby, the draft is too vanilla. We are an engineering team—we don't just describe what we built, we prove *why* we built it by exposing what failed first. Here is the exact strategy for the main agent to rewrite `PrototypeOverview.tex`.

## 1. Section 4 Pivot: "The Failure & Iteration Log"
We are changing the tone of Section 4 entirely. It should not read like a product manual ("Here is what it is"). It must read like an engineering iteration log ("Here is what failed, and here is how we fixed it").

### Mechanical Failures -> Solutions
*   **The Belt Slip:** The initial smooth TPU belt slipped continuously along the axle, rendering the carriage immobile. 
    *   *The Fix:* We designed an indented TPU belt with grip teeth (GT2 pitch) to lock into the pulley. 
    *   *Photos to use:* Show `OldTimingBelt.png` next to `BeltWithIndentations.HEIC`.
*   **The Axle Snap:** The V1 axles were too thin (teardrop FDM artifacts) and couldn't handle the compressive tension required to keep the belt taut. The axles physically bent and snapped.
    *   *The Fix:* Rihanna redesigned the axles to be significantly thicker with deeper belt slots.
    *   *Photos to use:* `V1vsV2PulleyAxle.HEIC` (This is crucial evidence of iteration).

### Electrical Failures -> Solutions
*   **The Brownout / Stall:** The original drivetrain used a 3-6V DC gearmotor driven by an L298N H-Bridge and powered by a 9V battery. It lacked the torque to pull the mass of the carriage and suffered massive voltage drops, resulting in severe motor jitter and stalling.
    *   *The Fix:* We completely segregated the power logic (5V logic, 12V motor) and pivoted to a Nema 17 stepper motor with an A4988 driver. We specifically tuned the A4988 VREF to 50% to prevent thermal shutdowns while maintaining holding torque.
    *   *Photos to use:* Contrast the failure `HBridge_Motor_Iteration2.jpeg` against the success `Stepper_A4988_ScrewTerminals_Final.jpeg`.

### Fluid Dynamics Pivot -> Solutions
*   **The Pulsed Flow Failure:** We originally planned to use a ball pump, but early testing proved it only provided pulsed, low-volume bursts that couldn't sustain shear stress.
    *   *The Fix:* Abstracted to a Dyson hairdryer to guarantee continuous, high-CFM flow, allowing us to focus on the nozzle geometry instead of pump mechanics.

## 2. Deepening the Justifications (The "Why")
The TAs will dock us if we don't justify our testing parameters. We need to lean heavily into *why* we made our testing choices, especially in Section 5.

*   **The Toilet Paper/Tissue Paper Analogue:** We didn't just use tissue paper because it was lying around. We need to explicitly state: *"Heavily saturated tissue paper was selected as a worst-case stiction analogue for wet leaves. Because saturated tissue possesses zero structural rigidity and maximizes surface contact area against the 40-grit sandpaper, it generates significantly higher stiction than an actual leaf. If our $30^\circ$ custom air blade can successfully peel wet tissue paper (as seen in `nozzle_wet_test.mov`), it exceeds the required force to clear standard organic roof debris."*
*   **The 40-Grit Sandpaper:** Justify this as a controlled, standardized friction analogue for asphalt shingles.
*   **The 30-Degree Angle:** Reiterate the aerodynamic vector decomposition. $>45^\circ$ pins the debris. $<15^\circ$ deflects over it. $30^\circ$ perfectly balances $F_y$ (Coanda-effect boundary attachment to get *under* the debris) with $F_x$ (tangential shear to push it down).

## 3. Better Photo Selection
The main agent must insert these exact file references into the LaTeX figures:
1.  **As-Built Full System:** Pull a frame from `Track_Short_Overview.mov` (or a similar wide shot if available) for Page 1.
2.  **Mechanical Iteration:** `V1vsV2PulleyAxle.HEIC` and `BeltWithIndentations.HEIC`.
3.  **Electrical Iteration:** `HBridge_Motor_Iteration2.jpeg` (labeled as "Failed DC/L298N Architecture") vs `Stepper_A4988_ScrewTerminals_Final.jpeg` (labeled as "Final Isolated Nema 17/A4988 Architecture").

**Main Agent Directive:** Rewrite Section 4 of `PrototypeOverview.tex` using the "What Failed -> How We Fixed It" framework. Inject the wet tissue paper justification into Section 5. Update all `\includegraphics` to use these specific files.
