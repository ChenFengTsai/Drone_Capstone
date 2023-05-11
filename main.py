from djitellopy import Tello
import speech_recognition as sr
from demo.up_down_voice import Voice_Detection


def main(drone1):
    # voice detection to fly
    vd = Voice_Detection(drone1)
    vd.fly_drones_voice()
    
    # gesture detection to trigger object detection
    
    
    # object dection to find ()
    
    
    
    # voice detection to land
    pass

if  __name__ == "__main__":
    # initilize the drone
    drone1 = Tello('192.168.86.27')
    drone1.connect()
    drone1.streamon()
    
    main(drone1)