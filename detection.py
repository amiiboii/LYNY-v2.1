import cv2
import numpy as np
import json
import mediapipe as mp
import requests
import time
import urllib.request
from line_profiler import LineProfiler


arduino_ip = "192.168.4.2"

# Define a list of commands
motor_commands = [
    "MOTOR1 1 0 255\nMOTOR2 1 0 255\n",  # Moving Forward
    "MOTOR1 0 1 255\nMOTOR2 0 1 255\n",  # Moving Backward
    "MOTOR1 1 1 0\nMOTOR2 1 1 255\n",      # Stopping
    "MOTOR1 1 0 150\nMOTOR2 1 0 255\n",  # Turning Left
    "MOTOR1 1 0 255\nMOTOR2 1 0 150\n",  # Turning Right
]

upCount = 0

mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4, 2)


with open('names_mapping.json', 'r') as json_file:
    names_mapping = json.load(json_file)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils



def get_detection_results():    
    
    # # Set the desired width and height for the resized frame
    width = 200
    height = 200

    url = "http://192.168.4.1"

    # Create a window for displaying the video feed
    cv2.namedWindow("Processed Video Feed", cv2.WINDOW_NORMAL)

    # Set a timeout value for the request (in seconds)
    timeout = 5
    byte_array = bytearray()


    # Open the URL as a video stream
    stream = urllib.request.urlopen(url, timeout=timeout)


    while True:
        
        global upCount, distance_to_centerline
        distance_to_centerline =0
        upCount = 0

        # Create an empty byte array to store the streamed content
        
        # Read the stream content in chunks
        chunk = stream.read(1024)

        # Break the loop if the stream is empty
        if not chunk:
            break

        # Append the chunk to the byte array
        byte_array.extend(chunk)

        # Search for the end of the frame marker
        i = byte_array.find(b'\xff\xd8')
        j = byte_array.find(b'\xff\xd9')
        
        # If both markers are found, decode the image
        if i != -1 and j != -1:
            frame_data = byte_array[i:j + 2]
            byte_array = byte_array[j + 2:]

            # Decode the image using OpenCV
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            # cv2.imshow("Processed Video Feed", frame)
            frame = cv2.resize(frame, (width, height))
            blob = cv2.dnn.blobFromImage(frame, 1.0, (width, height), (104.0, 177.0, 123.0))
            # net.setInput(blob)

            # Use the cv2.cuda module for GPU-accelerated operations
            # Note: This requires OpenCV built with CUDA support


            
            RGB_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(RGB_image)
            multiLandMarks = results.multi_hand_landmarks

            # Get the width and height of the frame
            width, height = frame.shape[1], frame.shape[0]
            # Calculate the centerline of the frame
            centerline_x = width // 2

            if multiLandMarks:
                handList = []
                for handLms in multiLandMarks:
                    mpDraw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                    for idx, lm in enumerate(handLms.landmark):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        handList.append((cx, cy))

                for point in handList:
                    cv2.circle(frame, point, 5, (255, 255, 0), cv2.FILLED)  # Smaller circles with radius 5

                for coordinate in finger_Coord:
                    if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                        upCount += 1
                if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
                    upCount += 1

                # Calculate the distance from the first finger to the centerline
                first_finger_x = handList[finger_Coord[0][0]][0]
                distance_to_centerline = (first_finger_x - centerline_x)

                cv2.putText(frame, str(upCount), (150, 150), cv2.FONT_HERSHEY_PLAIN, 12, (0, 255, 0), 12)
                cv2.putText(frame, f"Distance to Centerline: {distance_to_centerline}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow("Combined Frame", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            return distance_to_centerline, upCount


    cap.release()
    cv2.destroyAllWindows()



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
    distance_to_centerline, upCount = get_detection_results()
    print(f"Distance to Centerline: {distance_to_centerline}")
    print(f"UpCount: {upCount}")

    print("Determining action based on UpCount and Distance to Centerline...")

    if upCount == 3:
        print("Moving Forward")
        # send_commands("MOTOR1 1 0 255\nMOTOR2 1 0 255\n")
                # Additional logic for turning based on distance_to_centerline
        if distance_to_centerline < 0:
            print("Turning Right")
            # Adjust the motor commands for turning right
            send_commands("MOTOR1 1 0 150\nMOTOR2 1 0 200\n")
        elif distance_to_centerline > 0:
            print("Turning Left")
            # Adjust the motor commands for turning left
            send_commands("MOTOR1 1 0 200\nMOTOR2 1 0 150\n")
        else:
            print("No predefined action for the current UpCount and Distance to Centerline")
            send_commands("MOTOR1 1 0 255\nMOTOR2 1 0 255\n")

    elif upCount == 5:
        print("Stopping")
        send_commands("MOTOR1 1 1 0\nMOTOR2 1 1 0\n")

    elif upCount == 0:
        print("Moving Backward")
        send_commands("MOTOR1 0 1 150\nMOTOR2 0 1 150\n")

    else:
        print("Stopping")
        send_commands("MOTOR1 1 1 0\nMOTOR2 1 1 0\n")


    print("Waiting for the next iteration...")
    time.sleep(0)  # Adjust the sleep duration as needed