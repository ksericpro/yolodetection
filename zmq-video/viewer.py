import cv2
import zmq
import base64
import numpy as np

url = 'tcp://*:5555'
context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
print("Zmq Subscriber on {0}".format(url))
footage_socket.bind(url)
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode_(''))

while True:
    try:
        #frame = footage_socket.recv_string()
        #img = base64.b64decode(frame)
        #npimg = np.fromstring(img, dtype=np.uint8)
        #source = cv2.imdecode(npimg, 1)
        #cv2.imshow("Stream", source)
        #cv2.waitKey(1)

        frame = footage_socket.recv()
        npimg = np.frombuffer(frame, dtype=np.uint8)
        #npimg = npimg.reshape(480,640,3)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("Stream", source)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break