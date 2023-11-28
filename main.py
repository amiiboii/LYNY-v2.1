import cv2
import numpy as np
import json
import mediapipe as mp
import requests
import time

arduino_ip = "192.168.4.2"
upCount = 0

cap = cv2.VideoCapture(1)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands(min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4, 2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

led_status = "OFF"
prev_finger_count = 0
def get_detection_results():    

    width = 800
    height = 600
    threshold = 0.8
    while True:
        global upCount, distance_to_centerline
        distance_to_centerline =0
        upCount = 0
        
        ret, frame = cap.read()
        frame = cv2.resize(frame, (width, height))
        frame = cv2.flip(frame, 1)
        blob = cv2.dnn.blobFromImage(frame, 1.0, (width, height), (104.0, 177.0, 123.0))

        success, image = cap.read()
        RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        confidence_threshold = 0.5
        results = hands.process(RGB_image)
        multiLandMarks = results.multi_hand_landmarks
        width, height = frame.shape[1], frame.shape[0]
        centerline_x = width // 2

        if multiLandMarks:
            handList = []
            for handLms in multiLandMarks:
                mpDraw.draw_landmarks(frame, handLms, mp_Hands.HAND_CONNECTIONS)
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

            cv2.putText(frame, str(upCount), (150, 150), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 12)
            cv2.putText(frame, f"Distance to Centerline: {distance_to_centerline}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Combined Frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        return distance_to_centerline, upCount
    cap.release()
    cv2.destroyAllWindows()

def send_commands(commands):
    print(" ")
    print(" ")
    print(commands)
    url = f"http://{arduino_ip}/"
    try:
        response = requests.post(url, data=commands, timeout=0.25)
        response.raise_for_status()
        print(f"Sent commands: {commands.strip()} | Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error in sending commands: {e}")


def map_speed(value, low1, high1, low2, high2):
    return np.interp(value, [low1, high1], [low2, high2])

distance_to_centerline = 0
while True:
    distance_to_centerline, upCount == get_detection_results()
    print("\n\nDistance to centerline:", distance_to_centerline, "Up count:", upCount)

    if upCount == 3 or upCount == 4:
        print("Moving Forward")

        if distance_to_centerline >= 50:
            print("Turning Right")
            speed_motor1 = int(map_speed(abs(distance_to_centerline), 50, 200, 160, 170))
            speed_motor2 = int(map_speed(abs(distance_to_centerline), 50, 200, 190, 250))
            go = f"MOTOR1 1 0 {(speed_motor1)}\nMOTOR2 1 0 {(speed_motor2)}\n"

        elif distance_to_centerline <= -50:
            print("Turning Left")
            speed_motor2 = int(map_speed(abs(distance_to_centerline), 50, 200, 160, 170))
            speed_motor1 = int(map_speed(abs(distance_to_centerline), 50, 200, 190, 250))
            go = f"MOTOR1 1 0 {(speed_motor1)}\nMOTOR2 1 0 {(speed_motor2)}\n"

        else:
            print("Going Straight")
            go = "MOTOR1 1 0 255\nMOTOR2 1 0 255\n"

        send_commands(go)
        print(go)

    elif upCount == 5:
        print("Moving Backward")

        if distance_to_centerline >= 50:
            print("Moving Backward Right")
            speed_motor2 = int(map_speed(abs(distance_to_centerline), 50, 200, 160, 170))
            speed_motor1 = int(map_speed(abs(distance_to_centerline), 50, 200, 190, 250))
            go = f"MOTOR1 0 1 {(speed_motor1)}\nMOTOR2 0 1 {(speed_motor2)}\n"

        elif distance_to_centerline <= -50:
            print("Moving Backward Left")
            speed_motor1 = int(map_speed(abs(distance_to_centerline), 50, 200, 160, 170))
            speed_motor2 = int(map_speed(abs(distance_to_centerline), 50, 200, 190, 250))
            go = f"MOTOR1 0 1 {(speed_motor1)}\nMOTOR2 0 1 {(speed_motor2)}\n"

        else:
            print("Moving Backward Straight")
            go = "MOTOR1 0 1 255\nMOTOR2 0 1 255\n"
        
        send_commands(go)
        print(go)


    elif upCount == 0 or upCount == 1:
        print("Stopping")
        send_commands("MOTOR1 1 1 0\nMOTOR2 1 1 0\n")

    else:
        print("Stopping")
        send_commands("MOTOR1 1 1 0\nMOTOR2 1 1 0\n")



