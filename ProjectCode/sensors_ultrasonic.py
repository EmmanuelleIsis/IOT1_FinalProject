# src/sensors_ultrasonic.py

from gpiozero import DistanceSensor

# Adjust pins to your wiring
ultrasonic = DistanceSensor(echo=24, trigger=23, max_distance=4)

SENSOR_HEIGHT_CM = 30.0  # distance from sensor to bottom (tune this)

def read_water_level_cm():
    """
    Returns water level in cm (0 at bottom, increasing as water rises),
    or None on error.
    """
    try:
        distance_cm = ultrasonic.distance * 100.0
        water_level = max(0.0, SENSOR_HEIGHT_CM - distance_cm)
        return round(water_level, 2)
    except Exception as e:
        print(f"[ERROR] Ultrasonic read failed: {e}")
        return None
