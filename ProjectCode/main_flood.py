#!/usr/bin/env python3
import time
import json
import traceback

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import src.config as config
from src.mqtt_client import create_mqtt_client, publish_sample
from src.sensors_ds18b20 import read_ds18b20
from src.sensors_ultrasonic import read_water_level_cm
from src.state_machine import compute_state

def main():
    mqtt_client = create_mqtt_client()

    try:
        print("Connecting to AWS IoT...")
        mqtt_client.connect()
        print("Connected successfully!")
    except Exception as e:
        print("[FATAL] Could not connect to AWS IoT:", e)
        return

    print("Starting flood monitor loop. Press CTRL+C to stop.")

    try:
        while True:
            try:
                temp_c = read_ds18b20()
                distance_cm = read_water_level_cm()

                payload = {
                    "device_id": config.DEVICE_ID,
                    "temperature_c": temp_c if temp_c is not None else -99,
                    "water_level": distance_cm if distance_cm is not None else -1,
                    "state": compute_state(distance_cm),
                    "timestamp": int(time.time())
                }

                print("Publishing:", payload)
                mqtt_client.publish(config.TOPIC, json.dumps(payload), 1)

            except Exception as sensor_error:
                print("[ERROR] Sensor read or publish failed:", sensor_error)

            time.sleep(5)


    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    finally:
        print("Exiting cleanly.")

if __name__ == "__main__":
    main()
