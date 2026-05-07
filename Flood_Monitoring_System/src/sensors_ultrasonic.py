from gpiozero import DistanceSensor

ultrasonic = DistanceSensor(echo=24, trigger=23, max_distance=4)

SENSOR_HEIGHT_CM = 30.0  # tune if needed

def read_water_level_cm():
    try:
        distance_cm = ultrasonic.distance * 100.0
        water_level = max(0.0, SENSOR_HEIGHT_CM - distance_cm)
        return round(water_level, 2)
    except Exception as e:
        print(f"[ERROR] Ultrasonic read failed: {e}")
        return None
