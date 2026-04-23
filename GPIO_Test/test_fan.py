from gpiozero import Motor
import time
 
motor = Motor(forward=20, backward=21)
 
print("Motor test starting...")
 
print("Forward for 10 seconds...")
motor.forward()
time.sleep(10)
 
print("Stop for 2 seconds...")
motor.stop()
time.sleep(2)
 
print("Backward for 10 seconds...")
motor.backward()
time.sleep(10)
 
print("Final stop.")
motor.stop()
 
print("Test complete.")