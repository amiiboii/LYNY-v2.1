# LYNY-v2.1
Lyny is a small car project designed for remote control using both traditional methods through the Blynk app and cutting-edge hand gesture recognition using OpenCV. The hardware is built around an ESP32 microcontroller and an L298N motor driver, providing a versatile and interactive platform for experimentation.

## Blynk Firmware
Motor movements are determined based on joystick coordinates received through Blynk's virtual pin V2, adjusting motor speeds and directions accordingly. The code also includes hardware configurations, PWM setup for motor control, and LED indicators for Blynk connection status. Although there are commented-out sections related to potential additional features like button presses and analog joystick input, the primary focus is on Blynk-based control.

## Wifi/Motor Control communication firmware (firmware_car.ino)
This code establishes a simple web server on an ESP32, allowing external control of two motors. The motors are connected to pins 27, 26, 14 (Motor A), and 23, 22, 12 (Motor B). PWM is utilized for motor speed control, configured with channels 0 and 1, a frequency of 30,000 Hz, and a resolution of 8 bits. The device acts as an access point with SSID "ESP32-Access-Point" and password "123456789." The code continuously checks for incoming client connections. When a client connects, it reads commands until a newline character is received, processes the commands, and responds accordingly. Commands for each motor (MOTOR1 and MOTOR2) are structured as strings and include motor statuses and duty cycle information.

This code essentially turns the ESP32 into a motor controller accessible through a web browser. Clients can send commands to control the direction and speed of both motors by connecting to the ESP32's access point and sending appropriately formatted commands.

##Hand detection and Movemnts (main.py)
This Python script utilizes the OpenCV and MediaPipe libraries to capture video from a webcam and perform hand gesture recognition. The detected hand landmarks are used to calculate the number of extended fingers and the distance of the first finger from the centerline. This information is then translated into motor control commands for an Arduino connected to the same local network.

The script defines an arduino_ip variable representing the Arduino's IP address. It uses the MediaPipe library to detect hand landmarks, specifically tracking finger and thumb coordinates. The script continuously captures video frames, processes them, and calculates the number of extended fingers and the distance of the first finger from the centerline.

The send_commands function sends control commands to the Arduino using an HTTP POST request to the specified IP address. The map_speed function is used to map the distance to the desired speed range for motor control.

The main loop repeatedly calls the get_detection_results function to process hand gestures and then sends corresponding motor control commands to the Arduino based on the number of extended fingers and the finger's distance from the centerline. The script prints informative messages about the detected gestures and motor control actions.

Overall, this script enables real-time motor control of an Arduino-based system using hand gestures captured by a webcam. It provides dynamic responses to different hand configurations, allowing the user to control the movement of the connected device.

![IMG_5076](https://github.com/amiiboii/LYNY-v2.1/assets/121004983/0462f765-5f64-4dc4-ba93-96fce2648d51)
![IMG_5077](https://github.com/amiiboii/LYNY-v2.1/assets/121004983/e6be503f-7bee-4bcd-ba57-3d6996d96c43)

