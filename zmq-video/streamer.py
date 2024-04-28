from ultralytics import YOLO
import cv2
from cap_from_youtube import cap_from_youtube

import base64
import zmq

context = zmq.Context()
url = 'tcp://localhost:5555'
print("Zmq Publihser on {0}".format(url))
footage_socket = context.socket(zmq.PUB)
footage_socket.connect(url)

camera = cv2.VideoCapture(0)  # init the camera
print("Opening webcam")
while True:
    try:
        #grabbed, frame = camera.read()  # grab the current frame
        #frame = cv2.resize(frame, (640, 480))  # resize the frame
        #encoded, buffer = cv2.imencode('.jpg', frame)
        #jpg_as_text = base64.b64encode(buffer)
        #print("Sending {} bytes of data".format(len(jpg_as_text)))
        #footage_socket.send(jpg_as_text)

        grabbed, frame = camera.read()  # grab the current frame
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        footage_socket.send(buffer)
    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        print("An Error has occured")
        break