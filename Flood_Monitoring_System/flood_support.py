#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import glob
import time
import warnings
import tkinter as tk
import threading
import RPi.GPIO as GPIO 
from gpiozero import (
    DistanceSensor,
    LED,
    Button,
    RotaryEncoder,
    Motor
)
 
import flood
 
warnings.filterwarnings("ignore")
 
# =========================================================
# GPIO MODE
# =========================================================
 
GPIO.setmode(GPIO.BCM)
 
# =========================================================
# GLOBAL VARIABLES
# =========================================================
 
sensor = None
 
blue_led = None
yellow_led = None
red_led = None
 
fan = None
 
silence_button = None
manual_gate_button = None
 
encoder = None
 
buzzer = None
 
# =========================================================
# LANGUAGE SUPPORT
# =========================================================
 
current_lang = "EN"
 
LANG_DATA = {
 
    "EN": {
        "NORMAL": "NORMAL",
        "WARNING": "WARNING",
        "FLOOD": "FLOOD RISK",
        "TEMP": "Temperature",
        "LEVEL": "Water Level",
        "CRITICAL": "Critical Level",
        "SILENCE": "Silence\nAlarm",
        "GATE": "Manual Gate\nControl",
        "LANG": "Switch Language",
        "POWER": "ON/OFF"
    },
 
    "FR": {
        "NORMAL": "NORMAL",
        "WARNING": "ATTENTION",
        "FLOOD": "RISQUE CRUE",
        "TEMP": "Température",
        "LEVEL": "Niveau d'eau",
        "CRITICAL": "Niveau Critique",
        "SILENCE": "Silence\nAlarme",
        "GATE": "Contrôle\nManuel",
        "LANG": "Changer Langue",
        "POWER": "MARCHE"
    }
}
 
# =========================================================
# SYSTEM VARIABLES
# =========================================================
 
WARNING_LEVEL = 5
critical_level = 10
 
state = "NORMAL"
 
water_level = 0.0
temperature = 0.0
 
tank_height = 20
 
buzzer_silenced = False
manual_gate = False
system_enabled = True
 
last_warning_beep = 0
flood_alarm_running = False
 
# =========================================================
# HARDWARE INITIALIZATION
# =========================================================
 
def init_hardware():
 
    global sensor
    global blue_led
    global yellow_led
    global red_led
    global fan
    global silence_button
    global manual_gate_button
    global encoder
    global buzzer
 
    try:
 
        sensor = DistanceSensor(
            echo=24,
            trigger=23,
            max_distance=1
        )
 
        blue_led = LED(27)
        yellow_led = LED(17)
        red_led = LED(18)
 
        GPIO.setup(6, GPIO.OUT)
        buzzer = GPIO.PWM(6, 1000)
 
        fan = Motor(
            forward=21,
            backward=20
        )
 
        silence_button = Button(16)
        manual_gate_button = Button(5)
 
        encoder = RotaryEncoder(
            a=13,
            b=19,
            wrap=False,
            max_steps=30
        )
 
        silence_button.when_pressed = silence_alarm
        manual_gate_button.when_pressed = toggle_manual_gate
        encoder.when_rotated_clockwise = increase_critical_level
        encoder.when_rotated_counter_clockwise = decrease_critical_level
 
        print("Hardware initialized successfully")
 
    except Exception as e:
 
        print("Hardware Initialization Error:", e)
 
# =========================================================
# LANGUAGE SWITCH
# =========================================================
 
def switch_language():
 
    global current_lang
 
    current_lang = "FR" if current_lang == "EN" else "EN"
 
    l = LANG_DATA[current_lang]
 
    _w1.alarm_button.configure(text=l["SILENCE"])
    _w1.gate_button.configure(text=l["GATE"])
    _w1.lang_button.configure(text=l["LANG"])
    _w1.on_off_button.configure(text=l["POWER"])
 
    update_gui()
 
# =========================================================
# SYSTEM POWER
# =========================================================
 
def toggle_system():
 
    global system_enabled
 
    system_enabled = not system_enabled
 
    if not system_enabled:
 
        blue_led.off()
        yellow_led.off()
        red_led.off()
 
        fan.stop()
        buzzer.stop()
 
        _w1.display_label.configure(
            text="SYSTEM OFF",
            font=("Calibri", 9)
        )
 
        _w1.led_label.configure(
            text="OFF",
            background="gray",
            foreground="white"
        )
 
        print("System OFF")
 
    else:
        print("System ON")
 
# =========================================================
# ROTARY ENCODER
# =========================================================
 
def increase_critical_level():
 
    global critical_level
 
    critical_level += 1
 
    if critical_level > 20:
        critical_level = 20
 
    print(f"Critical Level: {critical_level} cm")
 
def decrease_critical_level():
 
    global critical_level
 
    critical_level -= 1
 
    if critical_level <= WARNING_LEVEL:
        critical_level = WARNING_LEVEL + 1
 
    print(f"Critical Level: {critical_level} cm")
 
# =========================================================
# TEMPERATURE SENSOR
# =========================================================
 
def read_temperature():
 
    global temperature
 
    try:
 
        device_folders = glob.glob('/sys/bus/w1/devices/28*')
 
        if not device_folders:
            return temperature
 
        device_file = device_folders[0] + '/w1_slave'
 
        with open(device_file, 'r') as f:
            lines = f.readlines()
 
        if lines[0].strip()[-3:] == 'YES':
 
            temp_pos = lines[1].find('t=')
 
            if temp_pos != -1:
 
                temperature = float(
                    lines[1][temp_pos + 2:]
                ) / 1000.0
 
    except Exception as e:
 
        print("Temperature Error:", e)
 
    return temperature
 
# =========================================================
# WATER LEVEL
# =========================================================
 
def read_water_level():
 
    global water_level
 
    try:
 
        distance_cm = sensor.distance * 100
 
        if distance_cm < 0:
            distance_cm = 0
 
        if distance_cm > tank_height:
            distance_cm = tank_height
 
        water_level = tank_height - distance_cm
 
    except Exception as e:
        print("Ultrasonic Error:", e)
 
    return water_level
 
# =========================================================
# STATE MACHINE
# =========================================================
 
def update_state():
 
    global state
 
    if water_level < WARNING_LEVEL:
        state = "NORMAL"
 
    elif WARNING_LEVEL <= water_level < critical_level:
        state = "WARNING"
 
    else:
        state = "FLOOD_RISK"
 
# =========================================================
# BUZZER FUNCTIONS
# =========================================================
 
def beep(freq=1000, duration=0.2):
 
    try:
        buzzer.ChangeFrequency(freq)
        buzzer.start(50)
        time.sleep(duration)
        buzzer.stop()
    except Exception as e:
        print("Buzzer Error:", e)
 
def warning_alarm():
 
    beep(700, 0.15)
    time.sleep(0.05)
    beep(900, 0.15)
    time.sleep(0.05)
    beep(1100, 0.20)
 
def flood_alarm():
 
    global flood_alarm_running
 
    if flood_alarm_running:
        return
 
    flood_alarm_running = True
 
    while state == "FLOOD_RISK" and not buzzer_silenced:
 
        beep(523, 0.15)
        time.sleep(0.05)
        beep(659, 0.15)
        time.sleep(0.05)
        beep(784, 0.20)
        time.sleep(0.05)
        beep(659, 0.15)
        time.sleep(0.05)
 
    flood_alarm_running = False
 
# =========================================================
# OUTPUT CONTROL
# =========================================================
 
def apply_outputs():
 
    global last_warning_beep
 
    if state == "NORMAL":
 
        blue_led.on()
        yellow_led.off()
        red_led.off()
 
        fan.stop()
        buzzer.stop()
 
    elif state == "WARNING":
 
        blue_led.off()
        yellow_led.on()
        red_led.off()
 
        fan.stop()
 
        current_time = time.time()
 
        if not buzzer_silenced:
 
            if current_time - last_warning_beep >= 2:
 
                threading.Thread(
                    target=warning_alarm,
                    daemon=True
                ).start()
 
                last_warning_beep = current_time
 
    elif state == "FLOOD_RISK":
 
        blue_led.off()
        yellow_led.off()
        red_led.on()
 
        if not manual_gate:
            try:
                fan.forward()
            except Exception as e:
                print("Fan Error:", e)
        else:
            fan.stop()
 
        if not buzzer_silenced:
 
            threading.Thread(
                target=flood_alarm,
                daemon=True
            ).start()
 
# =========================================================
# GUI UPDATE
# =========================================================
 
def update_gui():
 
    l = LANG_DATA[current_lang]
 
    _w1.display_label.configure(
 
        text=
        f"{l['TEMP']}: {temperature:.1f} °C\n\n"
        f"{l['LEVEL']}: {water_level:.1f} cm\n\n"
        f"{l['CRITICAL']}: {critical_level} cm",
 
        font=("Calibri", 9)
    )
 
    if state == "NORMAL":
 
        _w1.led_label.configure(
            text=l["NORMAL"],
            background="blue",
            foreground="white",
            font=("Calibri", 10, "bold")
        )
 
    elif state == "WARNING":
 
        _w1.led_label.configure(
            text=l["WARNING"],
            background="yellow",
            foreground="black",
            font=("Calibri", 10, "bold")
        )
 
    else:
 
        _w1.led_label.configure(
            text=l["FLOOD"],
            background="red",
            foreground="white",
            font=("Calibri", 10, "bold")
        )
 
# =========================================================
# BUTTON FUNCTIONS
# =========================================================
 
def silence_alarm():
 
    global buzzer_silenced
 
    buzzer_silenced = True
 
    buzzer.stop()
 
    print("Alarm silenced")
 
def toggle_manual_gate():
 
    global manual_gate
 
    manual_gate = not manual_gate
 
    if manual_gate:
 
        fan.stop()
 
        print("Manual gate enabled")
 
    else:
 
        print("Automatic gate enabled")
 
# =========================================================
# MAIN LOOP
# =========================================================
 
def update_system():
 
    global buzzer_silenced
 
    if system_enabled:
 
        read_water_level()
        read_temperature()
        update_state()
 
        if state == "NORMAL":
            buzzer_silenced = False
 
        apply_outputs()
        update_gui()
 
    root.after(500, update_system)
 
# =========================================================
# MAIN APPLICATION
# =========================================================
 
def main():
 
    global root
    global _w1
 
    try:
 
        init_hardware()
 
        root = tk.Tk()
 
        root.title("Flood Monitoring System")
 
        root.geometry("430x470")
 
        root.attributes("-topmost", False)
 
        _w1 = flood.Toplevel1(root)
 
        _w1.alarm_button.configure(command=silence_alarm)
        _w1.gate_button.configure(command=toggle_manual_gate)
        _w1.lang_button.configure(command=switch_language)
        _w1.on_off_button.configure(command=toggle_system)
 
        # =====================================================
        # ENABLE + AND - BUTTONS (PLACED EXACTLY LIKE GUI FILE)
        # =====================================================
 
        _w1.increase_button.configure(command=increase_critical_level)
        _w1.decrease_button.configure(command=decrease_critical_level)
 
        # EXACT SAME POSITION AS YOUR GUI FILE
        _w1.increase_button.place(x=250, y=220, width=47, height=26)
        _w1.decrease_button.place(x=150, y=220, width=47, height=26)
 
        # =====================================================
 
        root.after(500, update_system)
 
        root.mainloop()
 
    except Exception as e:
 
        print("Application Error:", e)
 
    finally:
 
        print("Cleaning up GPIO...")
 
        try:
 
            if sensor:
                sensor.close()
 
            if fan:
                fan.close()
 
            buzzer.stop()
 
            GPIO.cleanup()
 
        except Exception as e:
 
            print("Cleanup Error:", e)
 
# =========================================================
# START PROGRAM
# =========================================================
 
if __name__ == '__main__':
 
    main()