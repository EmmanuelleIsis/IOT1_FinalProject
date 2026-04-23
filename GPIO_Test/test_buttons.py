from gpiozero import LED, Button
from signal import pause
 
# 1. Initialize LEDs
led_red= LED(17)
led_blue = LED(18)
led_green = LED(27)
 
# Turn on the power indicator immediately
led_red.on()
 
# 2. Initialize Buttons
button_one = Button(4)
button_two = Button(5)
 
# 3. Define the Logic
# Button 1: Hold to turn on, release to turn off
button_one.when_pressed = led_blue.on
button_one.when_released = led_blue.off
 
# Button 2: Toggle mode (Press once for ON, press again for OFF)
button_two.when_pressed = led_green.toggle
 
 
print("System running with 3 LEDs and 2 Buttons.")
print("GPIO 17: Always ON")
print("GPIO 2  -> Controls GPIO 18 (Hold mode)")
print("GPIO 3  -> Controls GPIO 27 (Toggle mode)")
 
pause()