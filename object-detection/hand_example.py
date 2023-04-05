import cv2
import time
import numpy as np
from djitellopy import Tello

# Initialize the Tello drone
tello = Tello(host='192.168.86.33')
tello.connect()

# Start the video stream
tello.streamon()

# Load the MobileNetSSD object detection model for hand detection
model = cv2.dnn.readNetFromCaffe(
    'models/MobileNetSSD_deploy.prototxt',
    'models/MobileNetSSD_deploy.caffemodel'
)

# Set the initial speed and direction of the drone
x_speed = 0
y_speed = 0
z_speed = 0
yaw_speed = 0

# Set the distance from the drone to the hand
hand_distance = 150

# Define the class labels and colors for the MobileNetSSD model
classes = [
    'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair',
    'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
    'train', 'tvmonitor', 'hand'
]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loop until the user presses 'q' to quit
while True:
    # Get the frame from the video stream
    frame = tello.get_frame_read().frame

    # Prepare the frame for object detection by resizing it and normalizing the pixel values
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5
    )

    # Pass the frame through the object detection model to detect hands
    model.setInput(blob)
    detections = model.forward()

    # Find the hand detection with the highest confidence score
    max_confidence = 0
    hand_detection = None
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        class_id = int(detections[0, 0, i, 1])

        if confidence > 0.5 and classes[class_id] == 'hand':
            if confidence > max_confidence:
                max_confidence = confidence
                hand_detection = detections[0, 0, i, 3:7] * np.array([300, 300, 300, 300])

    # If a hand is detected, track it
    if hand_detection is not None:
        x1, y1, x2, y2 = hand_detection.astype(int)

        # Calculate the center of the hand
        hand_x = (x1 + x2) // 2
        hand_y = (y1 + y2) // 2

        # Draw a rectangle around the hand
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Calculate the error between the center of the frame and the center of the hand
        error_x = hand_x - 480
        error_y = hand_y - 360

        # Calculate the speed and direction of the drone based on the error
        x_speed = int(error_x / 16)
        y_speed = int(error_y / 16)
        z_speed = int(hand_distance / 10)
        yaw_speed = 0

        # Send the commands to the drone
        tello.send_rc_control(x_speed, y_speed, z_speed, yaw_speed)

    # Show the frame on the screen
    cv2.imshow('frame', frame)

    # Wait for 1 millisecond and check if the user pressed 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the video stream
tello.streamoff()

# Disconnect from the Tello drone
tello.disconnect()

# Close all OpenCV windows
cv2.destroyAllWindows()

