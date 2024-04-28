from ultralytics import YOLO
import cv2
from cap_from_youtube import cap_from_youtube
import signal

from typing import List

from fastapi import FastAPI, WebSocket
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect
import uvicorn
import threading, time
import base64
import asyncio

# global
_exit = False

# Load the YOLOv8 model
model = YOLO("../yolov8n.pt")

# Open youtube video
link = "https://www.youtube.com/watch?v=yHP-zGsoqRA "
cap = cap_from_youtube(link, "720p")

# api
app = FastAPI()
PORT = 8000

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Yolov8 Video Websocket</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        print("Client Connected")
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        print("Client Disconnected")
        self.connections.remove(websocket)

    async def _notify(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections


notifier = Notifier()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/push/{message}")
async def push_to_connected_websockets(message: str):
    await notifier.push(f"! Push notification: {message} !")
    return {"message": "message successfully broadcasted"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)

@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await notifier.generator.asend(None)
    #streaming_thread = threading.Thread(target=start_streaming, args=(notifier,))
    #streaming_thread.start()

    #_thread = threading.Thread(target=asyncio.run, args=(start_broadcast_msg(notifier),))
    #_thread.start()

    _streaming_thread = threading.Thread(target=asyncio.run, args=(start_streaming(notifier),))
    _streaming_thread.start()
    #_streaming_thread.join()
    

def handler(signum, frame):
    print("Ctrl-c was pressed")
    _exit = True
    exit(1)

async def start_streaming(_notifier):
    print("Starting Video Streaming...")
    start = time.time()
    # Loop through the video frames
    while cap.isOpened() and _exit==False:
        # Read a frame from the video
        success, frame = cap.read()
        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame)
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            #print(type(annotated_frame))
            processed_string = base64.b64encode(annotated_frame)
            #print(type(processed_string))
            #print(processed_string)
            #await _notifier.push("123")
            await _notifier.push(processed_string)
            #_notifier.push(f"123")
            # Display the annotated frame
            #cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            #if cv2.waitKey(1) & 0xFF == ord("q"):
            #    break
        else:
            # Break the loop if the end of the video is reached
            break
    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
    end = time.time()
    print('Execution Time: {}'.format(end-start))

async def start_broadcast_msg(_notifier):
    print("Starting broadcast_msg...")
    while True:
        await _notifier.push("123")
        time.sleep(1)


if __name__=="__main__":
    #start = time.time()
    signal.signal(signal.SIGINT, handler)
    #streaming_thread = threading.Thread(target=start_streaming, args=(notifier,))
    #apiserver_thread = threading.Thread(target=start_apiserver, args=(PORT,))
    uvicorn.run("youtube_stream_websocket:app",host='0.0.0.0', port=8000, reload=True, workers=3)
   # streaming_thread.start()
    #apiserver_thread.start()
    #uvicorn.run("youtube_stream_api:app",host='0.0.0.0', port=8000, reload=True, workers=3)

    #streaming_thread.join()
    #apiserver_thread.join()
    #end = time.time()
    #print('Execution Time: {}'.format(end-start))
   