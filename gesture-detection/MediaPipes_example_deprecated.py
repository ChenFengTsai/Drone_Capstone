import cv2
import mediapipe as mp
import numpy as np
import time
from djitellopy import Tello
import threading
import queue

# Initialize MediaPipe Hands and Tello drone
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drone = Tello('192.168.87.42')

# Connect to the drone
drone.connect()
print(f"Battery: {drone.get_battery()}%")

# Connect to the drone's video stream
drone.streamon()

# Define gestures and drone commands
def detect_gesture(landmarks):
    # Check if thumb tip is higher than thumb MCP joint (thumbs up)
    thumbs_up = landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.THUMB_MCP].y

    # Check if thumb tip is lower than thumb MCP joint (thumbs down)
    thumbs_down = landmarks[mp_hands.HandLandmark.THUMB_TIP].y > landmarks[mp_hands.HandLandmark.THUMB_MCP].y

    if thumbs_up:
        return "thumbs_up"
    elif thumbs_down:
        return "thumbs_down"
    else:
        return "none"

# Resize the input frame
def resize_frame(frame, scale_percent=50):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

# Throttle the frame rate
def limit_frame_rate(cap, fps=10):
    sleep_time = 1.0 / fps
    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        yield frame
        sleep_duration = sleep_time - (time.time() - start_time)
        if sleep_duration > 0:
            time.sleep(sleep_duration)

# Initialize the video capture with increased fifo_size and overrun_nonfatal option
print("Opening video capture")
cap = cv2.VideoCapture('udp://192.168.87.21:11111?fifo_size=50000000&overrun_nonfatal=1')
print("Video capture opened")



last_gesture_time = time.time()
in_air = False

frame_queue = queue.Queue(maxsize=1)

def process_frames():
    with mp_hands.Hands(min_detection_confidence=0.4, min_tracking_confidence=0.4, max_num_hands=1) as hands:
        while True:
            frame = frame_queue.get()
            if frame is None:
                break

            # Resize the frame before processing
            frame = resize_frame(frame)

            # Flip the frame horizontally for a later selfie-view display
            frame = cv2.flip(frame, 1)

            # Convert the BGR image to RGB before processing
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    gesture = detect_gesture(hand_landmarks.landmark)
                    print(f"Detected gesture: {gesture}")

                    current_time = time.time()
                    if current_time - last_gesture_time > 5:  # 5 seconds delay between gestures
                        if gesture == "thumbs_up" and not in_air:
                            drone.takeoff()
                            last_gesture_time = current_time
                            in_air = True
                        elif gesture == "thumbs_down" and in_air:
                            drone.land()
                            last_gesture_time = current_time
                            in_air = False

                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.imshow('Tello Camera Feed', frame)

            if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
                break

# Initialize a thread to process frames
process_thread = threading.Thread(target=process_frames)
process_thread.start()

# Use the limit_frame_rate generator to throttle the frame rate
for frame in limit_frame_rate(cap):
    frame_queue.put(frame)

    cv2.imshow('Tello Camera Feed', frame)

    if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Signal the processing thread to exit
frame_queue.put(None)
process_thread.join()

cap.release()
cv2.destroyAllWindows()
drone.streamoff()
drone.end()

