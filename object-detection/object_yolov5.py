import cv2
import numpy as np
import torch
from djitellopy import Tello
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box

def get_model(weights_path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path)
    return model

def preprocess_image(img, img_size=640):
    img = letterbox(img, new_shape=img_size)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float() / 255.0
    img = img.unsqueeze(0)
    return img

def process_detections(pred, conf_thres=0.25, iou_thres=0.45):
    pred = non_max_suppression(pred, conf_thres, iou_thres)
    return pred

def draw_boxes(img, det, names):
    for *xyxy, conf, cls in det:
        label = f'{names[int(cls)]} {conf:.2f}'
        plot_one_box(xyxy, img, label=label, color=(0, 255, 0), line_thickness=2)
    return img

# Load your YOLOv5 model
weights_path = '/Users/nicolasferreira/Documents/UChicago/Spring 2023/Capstone I/yolov5/yolov5s.pt'
model = get_model(weights_path)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device).eval()

# Connect to the Tello drone
tello = Tello('192.168.87.88')
tello.connect()
tello.streamon()

# Capture video from the Tello drone camera
cap = cv2.VideoCapture(tello.get_video_stream())

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the image and run it through the YOLOv5 model
    img = preprocess_image(frame)
    with torch.no_grad():
        pred = model(img)[0]

    # Process detections and draw bounding boxes on the image
    detections = process_detections(pred)
    if detections[0] is not None:
        frame = draw_boxes(frame, detections[0], model.module.names if hasattr(model, 'module') else model.names)

    # Display the image
    cv2.imshow('DJI Tello Live Object Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
tello.streamoff()
tello.end()
