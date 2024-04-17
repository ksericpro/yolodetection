from fastapi import WebSocket
from ultralytics import YOLO
import cv2
from fastapi import FastAPI, WebSocket

class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Direct Message"""
        await websocket.send_text(message)
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)

async def stream_camera(websocket, camera_num):
    # Load YOLO model
    model = YOLO('yolov8n.pt')
    vid = cv2.VideoCapture(camera_num, cv2.CAP_DSHOW)
    if not vid.isOpened():
        print(f"Failed to open camera {camera_num}")
        return

    try:
        while vid.isOpened():
            ret, frame = vid.read()
            if not ret:
                print(f"Failed to read frame from camera {camera_num}")
                break

            # Run YOLO detection on the frame
            results = model(frame)

            # Send the detection results to the client over the websocket connection
            await websocket.send(results)

    except Exception as e:
        print(f"Exception while streaming camera {camera_num}: {e}")
        pass


app = FastAPI()

manager = ConnectionManager()

@app.websocket("/communicate")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Received:{data}",websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_personal_message("Bye!!!",websocket)