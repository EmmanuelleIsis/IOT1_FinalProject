# src/sensors_ds18b20.py

import os

def read_ds18b20():
    base_dir = "/sys/bus/w1/devices/"
    try:
        device_folder = [d for d in os.listdir(base_dir) if d.startswith("28-")]
        if not device_folder:
            print("[ERROR] DS18B20 sensor not detected")
            return None

        device_file = os.path.join(base_dir, device_folder[0], "w1_slave")

        with open(device_file, "r") as f:
            lines = f.readlines()

        if "YES" not in lines[0]:
            print("[ERROR] DS18B20 CRC failed")
            return None

        temp_pos = lines[1].find("t=")
        if temp_pos != -1:
            temp_string = lines[1][temp_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return round(temp_c, 2)

        print("[ERROR] DS18B20 temperature data not found")
        return None

    except Exception as e:
        print(f"[ERROR] DS18B20 read failed: {e}")
        return None
