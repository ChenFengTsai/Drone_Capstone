import sys
import cv2
import torch
import numpy as np
from djitellopy import Tello

sys.path.append('./')  # Ensure the root folder of YOLOv5 repository is in the Python path

from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.datasets import letterbox
from utils.plots import plot_one_box


def process_frame(frame, model, device, imgsz):
    img = np.array(frame)

    img = letterbox(img, imgsz, stride=32)[0]
    img = img.transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    pred = model(img)[0]
    pred = non_max_suppression(pred, 0.25, 0.45, None, False)


    for *xyxy, conf, cls in reversed(pred[0]):
        label = f'{model.names[int(cls)]} {conf:.2f}'
        plot_one_box(xyxy, frame, label=label, color=(0, 255, 0), line_thickness=2)

    return frame

def main():
    weights = 'yolov5s.pt'
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = attempt_load(weights, map_location=device)
    imgsz = check_img_size(640, s=model.stride.max())
    model.to(device).eval()

    tello = Tello('192.168.86.31')
    tello.connect()
    tello.streamon()

    while True:
        frame = tello.get_frame_read().frame

        if frame is None:
            break

        frame = process_frame(frame, model, device, imgsz)
        cv2.imshow('DJI Tello Live Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    tello.streamoff()
    tello.end()

if __name__ == '__main__':
    main()
