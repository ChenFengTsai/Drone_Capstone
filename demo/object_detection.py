import sys
import cv2
import torch
import numpy as np
import time
from djitellopy import Tello
import configparser
from voice_detection import Voice_Detection

#config = configparser.ConfigParser()
#config.read('config.ini')
#yolov5_path = config.get('wifi', 'yolov5_path')

sys.path.append('./')
from yolov5 import *
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords
from yolov5.utils.datasets import letterbox
from yolov5.utils.plots import plot_one_box

class Object_Tracking:
    def __init__(self, drone, weights='yolov5s.pt'):
        self.weights = weights
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.imgsz = None
        self.drone = drone
        self.bottle_detected = False
        self.bottle_center = None
        self.box_size = None

    def initialize_drone(self):
        self.model = attempt_load(self.weights, map_location=self.device)
        self.imgsz = check_img_size(640, s=self.model.stride.max())
        self.model.to(self.device).eval()

        #self.drone.connect()
        #self.drone.streamon()
        print(f"Battery life percentage: {self.drone.get_battery()}%")
        #self.drone.takeoff()
        #time.sleep(5)

    def process_frame(self, frame):
        img = np.array(frame)
        h, w, _ = frame.shape
        img = letterbox(img, self.imgsz, stride=32)[0]
        img = img.transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = self.model(img)[0]
        pred = non_max_suppression(pred, 0.25, 0.45, None, False)

        self.bottle_detected = False
        self.bottle_center = None
        self.box_size = None
        for *xyxy, conf, cls in reversed(pred[0]):
            label = f'{self.model.names[int(cls)]} {conf:.2f}'
            if label.startswith('cup'):
                self.bottle_detected = True
                x_center = (xyxy[0] + xyxy[2]) / 2
                y_center = (xyxy[1] + xyxy[3]) / 2
                self.bottle_center = (x_center, y_center)

                # Get box width and height
                box_w = xyxy[2] - xyxy[0]
                box_h = xyxy[3] - xyxy[1]
                # Calculate box size (could also be box_w * box_h for box area)
                self.box_size = max(box_w, box_h)
                plot_one_box(xyxy, frame, label=label, color=(0, 255, 0), line_thickness=2)
        return frame

    def track_object(self):
        self.model = attempt_load(self.weights, map_location=self.device)
        self.imgsz = check_img_size(640, s=self.model.stride.max())
        self.model.to(self.device).eval()

        self.drone.connect()
        self.drone.streamon()
        #print(f"Battery life percentage: {self.drone.get_battery()}%")
        #self.drone.takeoff()
        time.sleep(3)
        #self.drone.rotate_clockwise(60)
        #self.drone.takeoff()
        found_bottle = False
        while not self.bottle_detected:
            self.drone.rotate_clockwise(45)
            time.sleep(3)

            frame = self.drone.get_frame_read().frame

            if frame is None:
                break

            frame = self.process_frame(frame)
            cv2.imshow('DJI Tello Live Object Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        while self.bottle_detected:
            frame = self.drone.get_frame_read().frame

            if frame is None:
                break

            frame = self.process_frame(frame)

            if not self.bottle_detected:
                self.drone.rotate_clockwise(45)
                time.sleep(3)
            else:
                # Assume that when box_size is 200, the drone is approximately 20cm away from the bottle
                if self.box_size < 200:
                    if self.bottle_center[0] < 320:
                        self.drone.move_left(20)
                    elif self.bottle_center[0] > 320:
                        self.drone.move_right(20)
                    if self.bottle_center[1] < 240:
                        self.drone.move_up(20)
                    elif self.bottle_center[1] > 240:
                        self.drone.move_down(20)
                    self.drone.move_forward(20)
                elif self.box_size > 200:
                    if self.bottle_center[0] < 320:
                        self.drone.move_left(20)
                    elif self.bottle_center[0] > 320:
                        self.drone.move_right(20)
                    if self.bottle_center[1] < 240:
                        self.drone.move_up(20)
                    elif self.bottle_center[1] > 240:
                        self.drone.move_down(20)
                    self.drone.move_backward(20)

                print('Voice detection started. Listening...')
                vd2 = Voice_Detection(self.drone)
                vd2.fly_drones_voice()
                print('Voice detection done')

            cv2.imshow('DJI Tello Live Object Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        self.drone.streamoff()
        self.drone.land()
