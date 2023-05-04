#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 18:21:33 2023

@author: miaya
"""

from djitellopy import Tello
import cv2
import numpy as np
import concurrent.futures
import speech_recognition as sr


def fly_drones_voice_3(drone1):
    # Connect to the first drone
    
   # drone2 = Tello(ip2)
    # Connect both drones
    
    #drone2.connect()
    # Start streaming from both drones
    
    #drone2.streamon()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        flip_forward1 = executor.submit(drone1.flip_forward)
        flip_forward1.result()
    

    # Create recognizer
    r = sr.Recognizer()
    mic = sr.Microphone()

    #Take off Drone to start
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     take_off1 = executor.submit(drone1.takeoff)
    #     take_off2 = executor.submit(drone2.takeoff)
    # drone1.rotate_clockwise(360)
    # drone2.rotate_counter_clockwise(360)

    # Continuously listen for the oral command
    while True:
        with mic as source:
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print(command)
            
            if "end" in command:
                break
            #elif "apple" in command:
                #with concurrent.futures.ThreadPoolExecutor() as executor:
                    #take_off1 = executor.submit(drone1.takeoff)
                   # take_off2 = executor.submit(drone2.takeoff)
                    #take_off1.result()
                   # take_off2.result()
            #elif "pan" in command:
                #with concurrent.futures.ThreadPoolExecutor() as executor:
                    #flip_forward1 = executor.submit(drone1.flip_forward)
                    #flip_forward2 = executor.submit(drone2.flip_forward)
                    #flip_forward1.result()
                   # flip_forward2.result()
            elif "turtle" in command:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    flip_rotate1 = executor.submit(drone1.rotate_clockwise)
                   # flip_rotate2 = executor.submit(drone2.rotate_counter_clockwise)
                    flip_rotate1.result(360)
                   # flip_rotate2.result(360)
            elif "land" in command:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    take_land1 = executor.submit(drone1.land)
                   # take_land2 = executor.submit(drone2.land)
                    take_land1.result()
                   # take_land2.result()
        except sr.UnknownValueError:
            continue
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        land1 = executor.submit(drone1.land)
        #land2 = executor.submit(drone2.land)
        land1.result()
        #land2.result()

drone1 = Tello('192.168.86.27')
drone1.connect()
drone1.streamon()
drone1.takeoff()
fly_drones_voice_3(drone1)