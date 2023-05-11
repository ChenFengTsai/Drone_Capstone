#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 20:44:19 2023

@author: miaya
"""


from djitellopy import Tello
import speech_recognition as sr


def fly_drones_voice_1(drone1):

    # Create recognizer
    r = sr.Recognizer()
    mic = sr.Microphone()

    # Continuously listen for the oral command
    while True:
        with mic as source:
            audio = r.listen(source, timeout = 10, phrase_time_limit = 3)
        try:
            
            command = r.recognize_google(audio).lower()
            print(command)
            if "land" in command:
                break
            elif "apple" in command:
                drone1.takeoff()
            else: 
                print("I don't understand the command")
        except sr.UnknownValueError:
            pass
        
    
    
drone1 = Tello('192.168.86.27')
drone1.connect()
drone1.streamon()
fly_drones_voice_1(drone1)
