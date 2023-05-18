from djitellopy import Tello
import speech_recognition as sr
from voice_detection import Voice_Detection
from gesture_detection import Gesture_Detection
import configparser

def main(drone, ip):
    # *voice detection to fly*
    vd = Voice_Detection(drone)
    vd.fly_drones_voice()
    print('voice detection done')
    
    # todo: gesture detection to trigger object detection
    gd = Gesture_Detection(drone, ip)
    gd.gesture_trigger()
    print('done')
    
    # todo: object dection to find ()
    
    
    
    
    # *voice detection to land*
    vd = Voice_Detection(drone)
    vd.fly_drones_voice()
    

if  __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    wifi_name = config.get('wifi', 'wifi_name')
    wifi_password = config.get('wifi', 'wifi_password')
    ip = config.get('wifi', '192.168.87.31')
    
    # initilize the drone
    drone = Tello(ip)
    drone.connect()
    drone.streamon()
    
    main(drone, ip)