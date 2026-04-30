from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(
    echo=24,
    trigger=23,
    max_distance=2,   # max 2 meters
    queue_len=5       # smooth readings
)

try:
    while True:
        distance = sensor.distance

        # Handle no echo / invalid readings
        if distance is None or distance >= 1:
            print("No echo / out of range")
        else:
            distance_cm = distance * 100

            # Ignore unrealistic values (too close or noise)
            if 2 <= distance_cm <= 200:
                print(f"Distance: {distance_cm:.2f} cm")
            else:
                print("Unstable reading")

        sleep(0.5)

except KeyboardInterrupt:
    print("Stopped")