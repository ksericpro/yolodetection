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


# Websocket Broadcast
- uvicorn test:app --reload
- open browser localhost:8000
- curl localhost:8000/push/test

# Links
- [Multithread] (https://www.dataquest.io/blog/multithreading-in-python/?utm_source=google&utm_medium=&matchtype=&device=c&utm_campaign=springsavings&campaignid=20758249356&adgroupid=&adid=&utm_content=&gad_source=1&gclid=CjwKCAjwoa2xBhACEiwA1sb1BIJkAmPYhXej4hHvd9fUMWx2HG0W3RducgePxtneu1Lw-1kBxlVFhBoCCMYQAvD_BwE)

- [Threads] (https://github.com/tiangolo/fastapi/issues/650)