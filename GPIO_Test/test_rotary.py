from gpiozero import RotaryEncoder, Button
from signal import pause
 
encoder = RotaryEncoder(a=13, b=19, max_steps=0)
 
button = Button(26)
 
def rotated():
    if encoder.steps > 0:
        print("Rotated clockwise")
    else:
        print("Rotated counter‑clockwise")
 
def pressed():
    print("Button pressed")
 
encoder.when_rotated = rotated
button.when_pressed = pressed
 
print("Rotary encoder test running...")
print("Rotate the knob or press the button.")
 
pause()