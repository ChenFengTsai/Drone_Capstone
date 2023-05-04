#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 20:44:19 2023

@author: miaya
"""
from djitellopy import Tello
#import concurrent.futures
import speech_recognition as sr


def fly_drones_voice_2(drone1):
    # Connect to the first drone
   # drone1 = Tello(ip1)
    #drone2 = Tello(ip2)
    # Connect both drones
    #drone1.connect()
    #drone2.connect()
    # Start streaming from both drones
   # drone1.streamon()
   # drone2.streamon()

    # Create recognizer
    r = sr.Recognizer()
    mic = sr.Microphone()
    drone1.takeoff()

    # Continuously listen for the oral command
    while True:
        with mic as source:
            audio = r.listen(source, timeout = 10, phrase_time_limit = 3)
        try:
            
            command = r.recognize_google(audio).lower()
            print(command)
            if "land" in command:
                break
            elif "banana" in command:
                drone1.move_forward(20)
                #drone2.takeoff()
            elif "apple" in command:
                drone1.flip_forward()
                #drone2.flip_forward()    
            elif "okay" in command:
                drone1.rotate_clockwise(360)
                #drone1.rotate_counterclockwise(360)
        except sr.UnknownValueError:
            continue
        
    #with concurrent.futures.ThreadPoolExecutor() as executor:
        # Fly forward for 50cm
        #move_forward1 = executor.submit(drone1.move_forward, 50)
        #move_forward2 = executor.submit(drone2.move_forward, 50)
        #move_forward1.result()
        #move_forward2.result()
        # Wait for 5 seconds
        #time.sleep(5)
    # Land the drones
    drone1.land()
    #drone2.land()
    
drone1 = Tello('192.168.86.')
drone1.connect()
drone1.streamon()
#drone1.takeoff()
fly_drones_voice_2(drone1)
