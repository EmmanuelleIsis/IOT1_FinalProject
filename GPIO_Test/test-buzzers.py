from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(18)

while True:
    print("Beep")
    buzzer.on()
    sleep(0.5)
    buzzer.off()
    sleep(1.5)