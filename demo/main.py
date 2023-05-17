from djitellopy import Tello
import speech_recognition as sr
from voice_detection import Voice_Detection
from gesture_detection import Gesture_Detection

def main(drone, ip):
    # *voice detection to fly*
    vd = Voice_Detection(drone)
    vd.fly_drones_voice()
    
    # todo: gesture detection to trigger object detection
    gd = Gesture_Detection(drone, ip)
    gd.gesture_trigger()
    
    # todo: object dection to find ()
    
    
    
    # *voice detection to land*
    vd = Voice_Detection(drone)
    vd.fly_drones_voice()
    

if  __name__ == "__main__":
    # initilize the drone
    ip = '192.168.87.31'
    drone = Tello(ip)
    drone.connect()
    drone.streamon()
    
    main(drone, ip)