# IOT1_FinalProject

Title: Internet of Things 1 Final Project

summary : 
In spring, temperature fluctuations and the melting of snow and ice cause water levels to rise, which can lead to significant property damage. However, if these changes are detected early, the resulting damage can be drastically reduced.
My team and I decided to develop an application to help users manage water levels and temperatures. The app evaluates flood risk, warns local users, and automatically activates a motorized flood gate when danger is detected. With this application, users can stay informed of potential hazards and avoid serious consequences.

How the app will work :

the water level will be in cm and this controls the system state 
the temperature will be in Celsius and this is for the telemetry only 
There are three states : Normal , Warning and Flood risk . The warning default level starts at 5 cm and at 10 cm, it becomes a critical. In the app , when the state is normal , the blue LED turns on, when the state is at warning , the yellow LED turns on and the buzzer beeps every two seconds. When the state is at flood risk the red LED turns on and the buzzer beeps continuously and the fan is on. Also, we decided to add a rotary encoder which will all  the user to manually set the critical water level. 

Features:

Hardware Components:

System Architecture:

GUI (image):

Installation Instructions and User Manual:


GUI  : update

When we click on the decrease button it displays in the display label, and the led change from yellow to green to simulate the normal temperature and safety with no alerts. Same for the increase button, when it is pressed it displays in the display label: Increase pressed and the led changes from green to yellow.

User manual : How to run the program?

First, we have the language button to switch from English to French and vice versa. On a label, we have the water level and the temperature that has been set. The water level can be changed using the increase and decrease button. We also have a WARNING label, for the critical levels. The Silence alarm button should be pressed to stop the buzzer and the control button is pressed to stop the gate and the fan.
We have the ON/OFF button to ON the system, and the OFF to switch OFF the system.

documentation of all the test

gui : connect the gui to the ras, and i run it in the terminal so when we press a button it will work , 
cloud : connect the temp and the sensor to the ras then publish the data amazon aws iot core  and the data got transfert to  amazon dynamo db and collected data
