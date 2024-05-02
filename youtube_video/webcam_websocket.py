from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from fastapi.templating import Jinja2Templates
import uvicorn
import asyncio
import cv2
# Install Fastapi, websockets, Jinja2
app = FastAPI()
#camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
camera = cv2.VideoCapture(0)

templates = Jinja2Templates(directory="templates")


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.03)
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")


if __name__ == '__main__':
    #uvicorn.run(app, host='127.0.0.1', port=8000)
    uvicorn.run(app, host='0.0.0.0', port=8000)