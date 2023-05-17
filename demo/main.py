from djitellopy import Tello
import speech_recognition as sr
from up_down_voice import Voice_Detection


def main(drone, ip):
    # voice detection to fly
    vd = Voice_Detection(drone)
    vd.fly_drones_voice()
    
    # gesture detection to trigger object detection
    
    
    
    # object dection to find ()
    
    
    
    # voice detection to land
    pass

if  __name__ == "__main__":
    # initilize the drone
    ip = '192.168.86.22'
    drone = Tello(ip)
    drone.connect()
    drone.streamon()
    
    main(drone, ip)