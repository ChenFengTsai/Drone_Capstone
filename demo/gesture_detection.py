# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 07:57:55 2023

@author: sb5
"""

import cv2
import mediapipe as mp
import numpy as np
import time
from djitellopy import Tello
from object_detection import Object_Tracking

# Initialize MediaPipe Hands and Tello drone
class Gesture_Detection:
    def __init__(self, drone, ip):
        self.drone = drone
        self.ip = ip
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        
    # Define gestures and drone commands
    def detect_gesture(self, landmarks):
        # Check if thumb tip is higher than thumb MCP joint (thumbs up)
        thumbs_up = landmarks[self.mp_hands.HandLandmark.THUMB_TIP].y < landmarks[self.mp_hands.HandLandmark.THUMB_MCP].y

        # Check if thumb tip is lower than thumb MCP joint (thumbs down)
        thumbs_down = landmarks[self.mp_hands.HandLandmark.THUMB_TIP].y > landmarks[self.mp_hands.HandLandmark.THUMB_MCP].y

        if thumbs_up:
            return "thumbs_up"
        elif thumbs_down:
            return "thumbs_down"
        else:
            return "none"

    def gesture_trigger(self):
        # Initialize the video capture
        cap = cv2.VideoCapture(f'udp://{self.ip}:11111')

        last_gesture_time = time.time()
        in_air = False

        with self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Failed to get frame")
                    break

                # Flip the frame horizontally for a later selfie-view display
                frame = cv2.flip(frame, 1)

                # Convert the BGR image to RGB before processing
                results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        gesture = self.detect_gesture(hand_landmarks.landmark)
                        print(f"Detected gesture: {gesture}")

                        current_time = time.time()
                        if current_time - last_gesture_time > 5:  # 5 seconds delay between gestures
                            if gesture == "thumbs_up" and not in_air:
                                #self.drone.takeoff()
                                print('Thumbs up detected. Object tracking initialized')
                                time.sleep(2)
                                cap.release()
                                self.drone.streamoff()
                                ot = Object_Tracking(self.drone)
                                ot.track_object()
                                last_gesture_time = current_time
                                in_air = True
                            elif gesture == "thumbs_down" and in_air:
                                self.drone.land()
                                last_gesture_time = current_time
                                in_air = False

                        self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                cv2.imshow('Tello Camera Feed', frame)

                if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
                    break

        cap.release()
        cv2.destroyAllWindows()
        self.drone.streamoff()
        self.drone.end()