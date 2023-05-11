# Import necessary libraries
from djitellopy import Tello
import cv2
from yolov5 import DetectionModel

# Initialize the drone and the YOLOv5 object detector
drone = Tello('192.168.87.88')
detector = DetectionModel()

# Connect to the drone
drone.connect()

# Start the video stream from the drone's camera
drone.streamon()

# Takeoff the drone
drone.takeoff()

# Loop through the frames of the video stream
while True:
    # Get the current frame from the video stream
    frame = drone.get_frame_read().frame
    
    # Use the DetectionModel to detect objects in the frame
    detections = detector.detect(frame)
    
    # Loop through the detected objects
    for detection in detections:
        # Check if the object is a backpack
        if detection.label == 'backpack':
            # Calculate the center of the object
            x_center = detection.x + detection.w // 2
            y_center = detection.y + detection.h // 2
            
            # Move the drone towards the object
            if x_center < frame.shape[1] // 2:
                drone.move_left(20)
            elif x_center > frame.shape[1] // 2:
                drone.move_right(20)
            if y_center < frame.shape[0] // 2:
                drone.move_up(20)
            elif y_center > frame.shape[0] // 2:
                drone.move_down(20)
    
    # Display the frame with the object bounding boxes
    cv2.imshow('Object Tracking', frame)
    
    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    
    # If the 'q' key is pressed, stop the loop and land the drone
    if key == ord('q'):
        break

# Land the drone and end the video stream
drone.land()
drone.streamoff()

# Close all windows
cv2.destroyAllWindows()