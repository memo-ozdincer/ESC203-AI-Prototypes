"""
ESC203 - Jinesis Group
Nema 17 Stepper Motor + A4988 Driver - Linear Track Controller
CircuitPython for Raspberry Pi Pico

Hardware:
  - Nema 17 stepper (1.8 deg/step, 200 steps/rev)
  - A4988 stepper driver (STEP, DIR, EN pins)
  - 12V DC wall adapter via barrel jack
  - Two Omron limit switches (NO) for absolute zeroing / failsafe
  - 60 cm track with GT2 belt + 20-tooth pulley (2mm pitch)

Wiring (screw-terminal / female-header layout):
  A4988 STEP  -> GP2
  A4988 DIR   -> GP3
  A4988 EN    -> GP4  (LOW = enabled)
  Limit SW Home (NO) -> GP5 (PULL_UP, wired to GND)
  Limit SW End  (NO) -> GP6 (PULL_UP, wired to GND)
"""

import board
import digitalio
import time
import usb_cdc

# ----- Pin Setup -----
pin_step = digitalio.DigitalInOut(board.GP2)
pin_step.direction = digitalio.Direction.OUTPUT
pin_step.value = False

pin_dir = digitalio.DigitalInOut(board.GP3)
pin_dir.direction = digitalio.Direction.OUTPUT
pin_dir.value = False

pin_enable = digitalio.DigitalInOut(board.GP4)
pin_enable.direction = digitalio.Direction.OUTPUT
pin_enable.value = True  # HIGH = disabled on startup

limit_home = digitalio.DigitalInOut(board.GP5)
limit_home.direction = digitalio.Direction.INPUT
limit_home.pull = digitalio.Pull.UP

limit_end = digitalio.DigitalInOut(board.GP6)
limit_end.direction = digitalio.Direction.INPUT
limit_end.pull = digitalio.Pull.UP

# ----- Motion Parameters -----
# GT2 belt: 2 mm pitch, 20-tooth pulley -> 40 mm per revolution
# 200 steps/rev (full-step) -> 0.2 mm per step
MM_PER_STEP = 0.2
TRACK_LENGTH_MM = 600  # 60 cm
STEPS_FULL_TRACK = int(TRACK_LENGTH_MM / MM_PER_STEP)  # 3000
STEP_DELAY_S = 0.0008  # ~625 steps/s

# Direction constants
DIR_FORWARD = True   # Toward END switch
DIR_BACKWARD = False  # Toward HOME switch

# State
current_step_position = 0


def home_pressed():
    return not limit_home.value  # Pulled HIGH, pressed = LOW


def end_pressed():
    return not limit_end.value


def enable_motor():
    pin_enable.value = False  # A4988: LOW = enabled


def disable_motor():
    pin_enable.value = True  # A4988: HIGH = disabled


def set_direction(direction):
    pin_dir.value = direction
    time.sleep(0.000005)  # A4988 setup time


def single_step(direction):
    """Pulse STEP once with limit-switch guard. Returns True if step taken."""
    if direction == DIR_FORWARD and end_pressed():
        return False
    if direction == DIR_BACKWARD and home_pressed():
        return False

    pin_step.value = True
    time.sleep(0.000005)
    pin_step.value = False
    time.sleep(STEP_DELAY_S)

    global current_step_position
    current_step_position += 1 if direction == DIR_FORWARD else -1
    return True


def move_steps(steps, direction):
    """Move N steps in a direction. Stops on limit switch. Returns steps taken."""
    set_direction(direction)
    taken = 0
    for _ in range(steps):
        if not single_step(direction):
            print("LIMIT SWITCH HIT - stopping")
            break
        taken += 1
    return taken


def move_millimeters(mm, direction):
    """Move a distance in mm."""
    steps = int(mm / MM_PER_STEP)
    return move_steps(steps, direction)


def home_track():
    """Drive backward until HOME switch triggers, then zero position."""
    print("Homing...")
    enable_motor()
    set_direction(DIR_BACKWARD)

    max_steps = STEPS_FULL_TRACK + 200
    for _ in range(max_steps):
        if home_pressed():
            print("Home switch triggered - zeroed.")
            global current_step_position
            current_step_position = 0
            disable_motor()
            return
        pin_step.value = True
        time.sleep(0.000005)
        pin_step.value = False
        time.sleep(STEP_DELAY_S)

    print("ERROR: Home switch not found within travel range!")
    disable_motor()


def full_pass():
    """Traverse home -> end -> home (air blade sweep)."""
    print("Starting full pass (home -> end -> home)...")
    enable_motor()

    fwd = move_steps(STEPS_FULL_TRACK, DIR_FORWARD)
    print(f"Forward steps taken: {fwd}")

    time.sleep(0.5)

    rev = move_steps(STEPS_FULL_TRACK, DIR_BACKWARD)
    print(f"Return steps taken: {rev}")

    disable_motor()
    print("Full pass complete.")


# ----- Main -----
print("=== Jinesis Track Controller (Pico) ===")
print("Commands: H=home, F=full pass, M=move 100mm fwd, B=move 100mm back")

disable_motor()
time.sleep(1)
home_track()

serial = usb_cdc.console

while True:
    if serial.in_waiting > 0:
        cmd = serial.read(1).decode("utf-8").upper()

        if cmd == "H":
            home_track()
        elif cmd == "F":
            full_pass()
        elif cmd == "M":
            enable_motor()
            move_millimeters(100.0, DIR_FORWARD)
            disable_motor()
        elif cmd == "B":
            enable_motor()
            move_millimeters(100.0, DIR_BACKWARD)
            disable_motor()

    time.sleep(0.01)  # Small sleep to avoid busy-waiting
