import cv2
import urllib.request
import numpy as np

url = "http://192.168.4.1"
cv2.namedWindow("Processed Video Feed", cv2.WINDOW_NORMAL)
timeout = 5
stream = urllib.request.urlopen(url, timeout=timeout)
byte_array = bytearray()

while True:
    chunk = stream.read(1024)
    if not chunk:
        break

    byte_array.extend(chunk)
    i = byte_array.find(b'\xff\xd8')
    j = byte_array.find(b'\xff\xd9')

    if i != -1 and j != -1:
        frame_data = byte_array[i:j + 2]
        byte_array = byte_array[j + 2:]
        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("Processed Video Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
