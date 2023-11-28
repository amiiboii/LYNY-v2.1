import requests
import time


arduino_ip = "192.168.4.3"

motor_commands = [
    "MOTOR1 1 0 255\nMOTOR2 1 0 255\n",  # Moving Forward
    "MOTOR1 0 1 255\nMOTOR2 0 1 255\n",  # Moving Backward
    "MOTOR1 1 1 0\nMOTOR2 1 1 255\n",      # Stopping
    "MOTOR1 1 0 150\nMOTOR2 1 0 255\n",  # Turning Left
    "MOTOR1 1 0 255\nMOTOR2 1 0 150\n",  # Turning Right
]

def send_commands(commands):
    url = f"http://{arduino_ip}/"
    try:
        response = requests.post(url, data=commands, timeout=0.2)
        response.raise_for_status()
        print(f"Sent commands: {commands.strip()} | Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error in sending commands: {e}")

while True:
    print("Getting detection results...")
    # Uncomment the following lines if needed
    # distance_to_centerline, upCount = get_detection_results()
    # print(f"Distance to Centerline: {distance_to_centerline}")
    # print(f"UpCount: {UpCount}")

    print("Sending commands to Arduino...")
    
    for command in motor_commands:
        send_commands(command)
        print(command)
        time.sleep(2)  
    print("Waiting for the next iteration...")
