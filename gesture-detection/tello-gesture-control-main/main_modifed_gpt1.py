#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 22:07:51 2023

@author: paryan414
"""

import cv2 as cv

from djitellopy import Tello
from gestures import *

import threading

def main():
    # init global vars
    global gesture_buffer
    global gesture_id
    global battery_status

    # Argument parsing
    args = get_args()
    KEYBOARD_CONTROL = args.is_keyboard
    WRITE_CONTROL = False
    in_flight = False

    # Camera preparation
    tello = Tello('192.168.1.211')
    tello.connect()
    tello.streamon()

    cap = tello.get_frame_read()

    # Init Tello Controllers
    gesture_controller = TelloGestureController(tello)

    gesture_detector = GestureRecognition(args.use_static_image_mode, args.min_detection_confidence,
                                          args.min_tracking_confidence)
    gesture_buffer = GestureBuffer(buffer_len=args.buffer_len)

    def tello_battery(tello):
        global battery_status
        try:
            battery_status = tello.get_battery()[:-2]
        except:
            battery_status = -1

    # FPS Measurement
    cv_fps_calc = CvFpsCalc(buffer_len=10)

    mode = 0
    battery_status = -1

    tello.move_down(20)

    while True:
        fps = cv_fps_calc.get()

        # Process Key (ESC: end)
        key = cv.waitKey(1) & 0xff
        if key == 27:  # ESC
            break

        # Camera capture
        image = cap.frame

        debug_image, gesture_id = gesture_detector.recognize(image, mode)
        gesture_buffer.add_gesture(gesture_id)

        gesture_controller.gesture_control(gesture_buffer)

        threading.Thread(target=tello_battery, args=(tello,)).start()

        debug_image = gesture_detector.draw_info(debug_image, fps, mode)

        # Battery status and image rendering
        cv.putText(debug_image, "Battery: {}".format(battery_status), (5, 720 - 5),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv.imshow('Tello Gesture Recognition', debug_image)

    tello.land()
    tello.end()
    cv.destroyAllWindows()
    
if __name__ == '__main__':
    main()

