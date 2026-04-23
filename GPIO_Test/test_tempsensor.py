import glob
import time
import os

BASE_DIR = '/sys/bus/w1/devices/'
REFERENCE_TEMP = 24.0

def find_sensor():
    devices = glob.glob(BASE_DIR + '28*')
    return devices[0] if devices else None

def read_raw_temp(device_file):
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return None

    # Validate reading
    if lines[0].strip()[-3:] != 'YES':
        return None

    temp_pos = lines[1].find('t=')
    if temp_pos != -1:
        return float(lines[1][temp_pos+2:]) / 1000.0

    return None

# Wait for sensor detection
device_folder = None
while device_folder is None:
    print("Searching for temperature sensor...")
    device_folder = find_sensor()
    if device_folder is None:
        time.sleep(2)

print(f"Sensor found: {device_folder}")
device_file = device_folder + '/w1_slave'

# Calibration phase
offset = None
while offset is None:
    raw = read_raw_temp(device_file)
    if raw is not None:
        offset = REFERENCE_TEMP - raw
        print(f"Calibration offset set to: {offset:.2f}")
    else:
        print("Waiting for valid reading...")
    time.sleep(1)

# Main loop
while True:
    raw = read_raw_temp(device_file)

    if raw is not None:
        calibrated = raw + offset
        print(f"Temperature: {calibrated:.2f} °C")
    else:
        print("Reading error...")

    time.sleep(1)
    