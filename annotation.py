from ultralytics.utils.plotting import Annotator
from ultralytics import YOLO
from PIL import Image
import cv2
import matplotlib.pyplot as plt

model_path = "D:/projects/pyprojects/yolo-detection/runs/detect/train3/weights/best.onnx"

print("model path={}".format(model_path))

model = YOLO(model_path)
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
#results = model.predict(source="0") # from video
#results = model.track(source="0", show=True)

# Process the image
image = "bus.jpg"
source = cv2.imread(image)
results = model(source)

# Extract results
annotator = Annotator(source, example=model.names)

#ann = Annotator(
#    image,
#    line_width=None,  # default auto-size
#    font_size=None,   # default auto-size
#    font="Arial.ttf", # must be ImageFont compatible
#    pil=False,        # use PIL, otherwise uses OpenCV
#)

result = results[0]
print(result.names)

print("{} boxes".format(len(result.boxes)))
#box = result.boxes[0]
ct=0
for box in result.boxes:
    ct = ct + 1
    print("box #{}".format(ct))
    #print("Object type:", box.cls[0])
    #print("Coordinates:", box.xyxy[0])
    #print("Probability:", box.conf[0])
    #cords = box.xyxy[0].tolist()
    #class_id = box.cls[0].item()
    #conf = box.conf[0].item()
    #print("Object type:", class_id)
    #print("Coordinates:", cords)
    #print("Probability:", conf)
    cords = box.xyxy[0].tolist()
    cords = [round(x) for x in cords]
    class_id = result.names[box.cls[0].item()]
    conf = round(box.conf[0].item(), 2)
    print("Object type:", class_id)
    print("Coordinates:", cords)
    print("Probability:", conf)


for box in results[0].boxes.xyxy.cpu():
    width, height, area = annotator.get_bbox_dimension(box)
    print("Bounding Box Width {}, Height {}, Area {}".format(
        width.item(), height.item(), area.item()))


plt.figure(figsize=(10,10))
plt.imshow(source)
plt.show()

#results = model.predict(source="folder", show=True) # Display preds. Accepts all YOLO predict arguments

# from PIL
#im1 = Image.open("bus.jpg")
#results = model.predict(source=im1, save=True)  # save plotted images

# from ndarray
#im2 = cv2.imread("bus.jpg")
#results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# from list of PIL/ndarray
#results = model.predict(source=[im1, im2])