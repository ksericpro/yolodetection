# Link

-[yolo] (https://github.com/ultralytics/ultralytics)
-[more yolo example] (https://docs.ultralytics.com/usage/python/)
-[flask api + html] (https://www.freecodecamp.org/news/how-to-detect-objects-in-images-using-yolov8/)
-*[real time you tube stream] (https://docs.salad.com/docs/yolov8-deployment-tutorial)
-[front end websocket] (https://alpha2phi.medium.com/yolo-using-fastapi-websocket-and-react-2b2d28e9f7ed)
- [Websocket] (https://github.com/ultralytics/ultralytics/issues/1102)
- [Fastap + WebSocket](https://medium.com/@nmjoshi/getting-started-websocket-with-fastapi-b41d244a2799)
- [issue] (https://github.com/tiangolo/fastapi/issues/258)
- [Lifespan] (https://fastapi.tiangolo.com/advanced/events/)

# Setup

## direct
- yolo predict model=yolov8n.pt source='https://ultralytics.com/images/bus.jpg'

## Train sand save model
- Results saved to D:\projects\pyprojects\yolo-detection\runs\detect\train3\weights


## Run flask API
- python object_detector.py

## open browser
- localhost:8080


## run fast api
- uvicorn fastapi_websocket:app --reload
- unvicron test:app --reload
- curl localhost:8000/push/testfdfd