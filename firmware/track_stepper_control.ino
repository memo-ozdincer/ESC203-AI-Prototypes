/*
 * ESC203 - Jinesis Group
 * Nema 17 Stepper Motor + A4988 Driver - Linear Track Controller
 *
 * Hardware:
 *   - Nema 17 stepper (1.8 deg/step, 200 steps/rev)
 *   - A4988 stepper driver (STEP, DIR, EN pins)
 *   - 12V DC wall adapter via barrel jack
 *   - Two Omron limit switches (NO) for absolute zeroing / failsafe
 *   - 60 cm track with GT2 belt + 20-tooth pulley (2mm pitch)
 *
 * Wiring (match screw-terminal / female-header layout):
 *   A4988 STEP  -> Arduino pin 3
 *   A4988 DIR   -> Arduino pin 4
 *   A4988 EN    -> Arduino pin 5  (LOW = enabled)
 *   Limit SW Home (NO) -> Arduino pin 6 (INPUT_PULLUP, wired to GND)
 *   Limit SW End  (NO) -> Arduino pin 7 (INPUT_PULLUP, wired to GND)
 */

// ----- Pin Definitions -----
const int PIN_STEP      = 3;
const int PIN_DIR       = 4;
const int PIN_ENABLE    = 5;
const int PIN_LIMIT_HOME = 6;   // Normally-open, pulled HIGH; pressed = LOW
const int PIN_LIMIT_END  = 7;

// ----- Motion Parameters -----
// GT2 belt: 2 mm pitch, 20-tooth pulley -> 40 mm per revolution
// 200 steps/rev (full-step) -> 0.2 mm per step
const float MM_PER_STEP       = 0.2;
const int   TRACK_LENGTH_MM   = 600;          // 60 cm
const int   STEPS_FULL_TRACK  = (int)(TRACK_LENGTH_MM / MM_PER_STEP);  // 3000
const int   STEP_DELAY_US     = 800;          // microseconds between pulses (~625 steps/s)

// ----- Direction Constants -----
const bool DIR_FORWARD  = HIGH;   // Toward END switch
const bool DIR_BACKWARD = LOW;    // Toward HOME switch

// ----- State -----
volatile bool eStopTriggered = false;
int currentStepPosition = 0;      // 0 = home

// ============================================================
// Helpers
// ============================================================

bool homePressed()  { return digitalRead(PIN_LIMIT_HOME) == LOW; }
bool endPressed()   { return digitalRead(PIN_LIMIT_END)  == LOW; }

void enableMotor()  { digitalWrite(PIN_ENABLE, LOW);  }
void disableMotor() { digitalWrite(PIN_ENABLE, HIGH); }

void setDirection(bool dir) {
  digitalWrite(PIN_DIR, dir);
  delayMicroseconds(5);  // A4988 setup time
}

// Single step pulse with limit-switch guard.
// Returns true if step was taken, false if blocked by limit switch.
bool singleStep(bool dir) {
  // Safety: do not move into a tripped switch
  if (dir == DIR_FORWARD && endPressed())  return false;
  if (dir == DIR_BACKWARD && homePressed()) return false;

  digitalWrite(PIN_STEP, HIGH);
  delayMicroseconds(5);
  digitalWrite(PIN_STEP, LOW);
  delayMicroseconds(STEP_DELAY_US);

  // Track position
  currentStepPosition += (dir == DIR_FORWARD) ? 1 : -1;
  return true;
}

// Move a given number of steps in a direction.
// Stops early if a limit switch is hit.
// Returns actual steps taken.
int moveSteps(int steps, bool dir) {
  setDirection(dir);
  int taken = 0;
  for (int i = 0; i < steps; i++) {
    if (!singleStep(dir)) {
      Serial.println("LIMIT SWITCH HIT - stopping");
      break;
    }
    taken++;
  }
  return taken;
}

// Move a distance in millimeters.
int moveMillimeters(float mm, bool dir) {
  int steps = (int)(mm / MM_PER_STEP);
  return moveSteps(steps, dir);
}

// ============================================================
// Homing Routine - drives backward until HOME switch is pressed
// ============================================================
void homeTrack() {
  Serial.println("Homing...");
  enableMotor();
  setDirection(DIR_BACKWARD);

  // Move backward until home switch triggers (max STEPS_FULL_TRACK + margin)
  int maxSteps = STEPS_FULL_TRACK + 200;
  for (int i = 0; i < maxSteps; i++) {
    if (homePressed()) {
      Serial.println("Home switch triggered - zeroed.");
      currentStepPosition = 0;
      disableMotor();
      return;
    }
    digitalWrite(PIN_STEP, HIGH);
    delayMicroseconds(5);
    digitalWrite(PIN_STEP, LOW);
    delayMicroseconds(STEP_DELAY_US);
  }

  // If we get here, home was never found
  Serial.println("ERROR: Home switch not found within travel range!");
  disableMotor();
}

// ============================================================
// Full Pass - traverse home -> end -> home (air blade sweep)
// ============================================================
void fullPass() {
  Serial.println("Starting full pass (home -> end -> home)...");
  enableMotor();

  // Forward sweep
  int fwd = moveSteps(STEPS_FULL_TRACK, DIR_FORWARD);
  Serial.print("Forward steps taken: ");
  Serial.println(fwd);

  delay(500);  // Brief pause at end of track

  // Return sweep
  int rev = moveSteps(STEPS_FULL_TRACK, DIR_BACKWARD);
  Serial.print("Return steps taken: ");
  Serial.println(rev);

  disableMotor();
  Serial.println("Full pass complete.");
}

// ============================================================
// Setup & Loop
// ============================================================
void setup() {
  Serial.begin(9600);

  pinMode(PIN_STEP,       OUTPUT);
  pinMode(PIN_DIR,        OUTPUT);
  pinMode(PIN_ENABLE,     OUTPUT);
  pinMode(PIN_LIMIT_HOME, INPUT_PULLUP);
  pinMode(PIN_LIMIT_END,  INPUT_PULLUP);

  disableMotor();
  digitalWrite(PIN_STEP, LOW);
  digitalWrite(PIN_DIR,  LOW);

  delay(1000);
  Serial.println("=== Jinesis Track Controller ===");
  Serial.println("Commands: H=home, F=full pass, M=move 100mm fwd, B=move 100mm back");

  // Auto-home on startup
  homeTrack();
}

void loop() {
  if (Serial.available()) {
    char cmd = toupper(Serial.read());

    switch (cmd) {
      case 'H':
        homeTrack();
        break;
      case 'F':
        enableMotor();
        fullPass();
        disableMotor();
        break;
      case 'M':
        enableMotor();
        moveMillimeters(100.0, DIR_FORWARD);
        disableMotor();
        break;
      case 'B':
        enableMotor();
        moveMillimeters(100.0, DIR_BACKWARD);
        disableMotor();
        break;
      default:
        break;
    }
  }
}
