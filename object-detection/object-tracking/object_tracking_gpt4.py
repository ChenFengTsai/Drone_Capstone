import sys
import cv2
import torch
import numpy as np
import time
from djitellopy import Tello

sys.path.append('./')

from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.datasets import letterbox
from utils.plots import plot_one_box

def process_frame(frame, model, device, imgsz):
    img = np.array(frame)
    h, w, _ = frame.shape
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

    bottle_detected = False
    bottle_center = None
    box_size = None
    for *xyxy, conf, cls in reversed(pred[0]):
        label = f'{model.names[int(cls)]} {conf:.2f}'
        if label.startswith('cup'):
            bottle_detected = True
            x_center = (xyxy[0] + xyxy[2]) / 2
            y_center = (xyxy[1] + xyxy[3]) / 2
            bottle_center = (x_center, y_center)

            # Get box width and height
            box_w = xyxy[2] - xyxy[0]
            box_h = xyxy[3] - xyxy[1]
            # Calculate box size (could also be box_w * box_h for box area)
            box_size = max(box_w, box_h)
            plot_one_box(xyxy, frame, label=label, color=(0, 255, 0), line_thickness=2)
    return frame, bottle_detected, bottle_center, box_size

def main():
    weights = 'yolov5s.pt'
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = attempt_load(weights, map_location=device)
    imgsz = check_img_size(640, s=model.stride.max())
    model.to(device).eval()

    tello = Tello('192.168.86.29')
    tello.connect()
    tello.streamon()

    print(f"Battery life percentage: {tello.get_battery()}%")

    tello.takeoff()
    time.sleep(5)

    found_bottle = False
    while not found_bottle:
        tello.rotate_clockwise(45)
        time.sleep(3)

        frame = tello.get_frame_read().frame

        if frame is None:
            break

        frame, found_bottle, _, _ = process_frame(frame, model, device, imgsz)
        cv2.imshow('DJI Tello Live Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    while found_bottle:
        frame = tello.get_frame_read().frame

        if frame is None:
            break

        frame, bottle_detected, bottle_center, box_size = process_frame(frame, model, device, imgsz)

        if not bottle_detected:
            tello.rotate_clockwise(45)
            time.sleep(3)
        else:
            # Assume that when box_size is 200, the drone is approximately 20cm away from the bottle
            if box_size < 200:
                if bottle_center[0] < 320:
                    tello.move_left(20)
                elif bottle_center[0] > 320:
                    tello.move_right(20)
                if bottle_center[1] < 240:
                    tello.move_up(20)
                elif bottle_center[1] > 240:
                    tello.move_down(20)
                tello.move_forward(20)
            elif box_size > 200:
                if bottle_center[0] < 320:
                    tello.move_left(20)
                elif bottle_center[0] > 320:
                    tello.move_right(20)
                if bottle_center[1] < 240:
                    tello.move_up(20)
                elif bottle_center[1] > 240:
                    tello.move_down(20)
                tello.move_back(20)

        cv2.imshow('DJI Tello Live Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    tello.streamoff()
    tello.land()

if __name__ == '__main__':
    main()

