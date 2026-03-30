import board
import digitalio
import time

# Setting up the buttons
left = digitalio.DigitalInOut(board.GP15)
left.direction = digitalio.Direction.INPUT
left.pull = digitalio.Pull.UP

right = digitalio.DigitalInOut(board.GP16)
right.direction = digitalio.Direction.INPUT
right.pull = digitalio.Pull.UP

# Setting up the stepper board pins
en = digitalio.DigitalInOut(board.GP0)
en.direction = digitalio.Direction.OUTPUT
en.value = False

step = digitalio.DigitalInOut(board.GP1) 
step.direction = digitalio.Direction.OUTPUT

dir = digitalio.DigitalInOut(board.GP2)
dir.direction = digitalio.Direction.OUTPUT
dir.value = False

# Variable to count how many times the air blade travels
cycle: int = 0

 
while True:
    
    # Debugging feature, so if you press both buttons it resets and moves
    if left.value == False and right.value == False:
        cycle = 0
    
    # Line to stop moving, because stepper needs to be able to switch between on and off in the "step" pin to move, and this just skips that
    if cycle == 4:
        continue
    
    if left.value == False:
        dir.value = True
        cycle += 1
        time.sleep(0.25)
        
    if right.value == False:
        dir.value = False
        cycle += 1
        time.sleep(0.25)
    
    step.value = True
    time.sleep(0.005)
    step.value = False
    time.sleep(0.005)
        