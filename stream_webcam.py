from ultralytics import YOLO
import cv2

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