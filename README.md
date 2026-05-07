# IOT1_FinalProject

## Title
Flood Monitoring System

---

# Summary

summary : 
In spring, temperature fluctuations and the melting of snow and ice cause water levels to rise, which can lead to significant property damage. However, if these changes are detected early, the resulting damage can be drastically reduced.
My team and I decided to develop an application to help users manage water levels and temperatures. The app evaluates flood risk, warns local users, and automatically activates a motorized flood gate when danger is detected. With this application, users can stay informed of potential hazards and avoid serious consequences.

---

# How the App Works

- The water level is measured in centimeters (cm) and controls the system state.
- The temperature is measured in Celsius (°C) and is used only for telemetry.
- The system has three states:
  - **Normal**
  - **Warning**
  - **Flood Risk**

### State Behavior

## Normal State
- Blue LED turns ON
- Fan is OFF
- Buzzer is OFF

## Warning State
- Activated when water level reaches 5 cm
- Yellow LED turns ON
- Buzzer beeps every 2 seconds
- Fan remains OFF

## Flood Risk State
- Activated when water level reaches the critical level (default = 10 cm)
- Red LED turns ON
- Buzzer sounds continuously
- Fan turns ON automatically

A rotary encoder and GUI buttons allow the user to manually adjust the critical flood level.

---

# Features

- Real-time water level monitoring
- Temperature telemetry display
- Three-state flood detection system
- LED visual indicators
- Continuous and warning alarm system
- Motorized flood gate/fan activation
- Manual gate control
- Rotary encoder support
- GUI critical level controls
- English/French language switching
- ON/OFF system control

---

# Hardware Components

![alt text](<Hardware Inventory.png>)

- Raspberry Pi
- Ultrasonic Distance Sensor
- Temperature Sensor
- Passive Buzzer
- Blue LED
- Yellow LED
- Red LED
- DC Fan / Motor
- Motor Driver Module (L298N/L293D/TB6612)
- Rotary Encoder
- Push Buttons
- Breadboard and Jumper Wires

---

# System Architecture

![alt text](<System Architecture Diagram.png>)

## GPIO Connections

| Component | GPIO Pins |
|---|---|
| Ultrasonic Trigger | GPIO 23 |
| Ultrasonic Echo | GPIO 24 |
| Blue LED | GPIO 27 |
| Yellow LED | GPIO 17 |
| Red LED | GPIO 18 |
| Passive Buzzer | GPIO 6 |
| Fan Driver IN1 | GPIO 21 |
| Fan Driver IN2 | GPIO 20 |
| Silence Button | GPIO 16 |
| Manual Gate Button | GPIO 5 |
| Rotary Encoder A | GPIO 13 |
| Rotary Encoder B | GPIO 19 |

---

# GUI

![alt text](<GUI Image.png>)

---

# Installation Instructions

## 1. Clone the Repository

```bash
git clone <your-repository-link>
cd <The folder name>
```

## 2. Install Required Libraries

```bash
pip install gpiozero
pip install RPi.GPIO
```

## 3. Enable GPIO Interfaces

Enable:
- GPIO
- 1-Wire Interface

Using:

```bash
sudo raspi-config
```

Then reboot the Raspberry Pi.

---

# User Manual

## Starting the System

Run the application using: Open RealVNC Viewer, then connect to the Raspberry Pi, and run the following command:

```bash
export DISPLAY=:0
python3 main.py
```

---

## Using the System

### Normal State
- Blue LED indicates safe water level.

### Warning State
- Yellow LED indicates rising water level.
- Buzzer beeps every 2 seconds.

### Flood Risk State
- Red LED indicates dangerous water level.
- Continuous buzzer alarm activates.
- Fan/flood gate activates automatically.

---

## Buttons

### Silence Alarm Button
- Stops the buzzer temporarily.

### Manual Gate Control Button
- Enables or disables automatic fan/flood gate operation.

### Increase/Decrease Buttons
- Adjust the critical flood level manually.

### Rotary Encoder
- Also adjusts the critical flood level.

### ON/OFF Button
- Turns the monitoring system ON or OFF.

### Language Button
- Switches between English and French.

---

the water level will be in cm and this controls the system state 
the temperature will be in Celsius and this is for the telemetry only 
There are three states : Normal , Warning and Flood risk . The warning default level starts at 5 cm and at 10 cm, it becomes a critical. In the app , when the state is normal , the blue LED turns on, when the state is at warning , the yellow LED turns on and the buzzer beeps every two seconds. When the state is at flood risk the red LED turns on and the buzzer beeps continuously and the fan is on. Also, we decided to add a rotary encoder which will all  the user to manually set the critical water level. 

Features:

Hardware Components:

System Architecture:

GUI (image):

Installation Instructions and User Manual:
button