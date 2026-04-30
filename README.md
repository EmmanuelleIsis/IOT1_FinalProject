# IOT1_FinalProject

Title: Flood Monitoring System

Summary : 
During the spring season, rapid temperature fluctuations and melting snow often lead to rising water levels and significant property damage; however, early detection can drastically reduce these risks. Our team developed an IoT application designed to help users monitor and manage these environmental changes by evaluating flood risks, issuing immediate warnings, and automatically activating a motorized flood gate when danger is detected. This system operates based on real-time sensor inputs, primarily utilizing water level measurements in centimeters to dictate the system state, while temperature data in Celsius is collected for telemetry and tracking. To ensure flexibility, we integrated a rotary encoder, allowing users to manually adjust the critical water level threshold to suit specific environmental needs. The application is designed to be user-friendly, with a simple and intuitive interface that enables users to quickly and easily monitor the flood risks and take appropriate action.

How the app will work :
The application functions through three distinct operational states that trigger specific hardware responses to keep users informed. In the Normal State, characterized by water levels below 5 cm, a blue LED remains illuminated to indicate safety with no active alerts. Once the water level reaches the 5 cm warning threshold, a yellow LED activates and a buzzer beeps at two-second intervals to signal caution. If the water reaches the 10 cm critical threshold or the user-defined limit set by the rotary encoder, the system enters the Flood Risk state, which triggers a red LED, continuous buzzing for maximum urgency, and the activation of a fan to simulate the deployment of a motorized flood gate.

Features:

Hardware Components:

![alt text](<Hardware Components.png>)

System Architecture:

![alt text](<System Architecture.png>)

GUI (image):

![alt text](<GUI Image.png>)

Installation Instructions and User Manual: