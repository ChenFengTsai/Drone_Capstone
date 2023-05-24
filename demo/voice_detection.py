#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 20:44:19 2023

@author: miaya
"""
from djitellopy import Tello
import speech_recognition as sr


class Voice_Detection:
    def __init__(self, drone):
        self.drone = drone

    def fly_drones_voice(self):
        # Create recognizer
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        # Listen for the oral command
        with mic as source:
            audio = r.listen(source, timeout = 10, phrase_time_limit = 3)
        try:   
            command = r.recognize_google(audio).lower()
            print(f'Command found: {command}')
            
            if "chicken" in command:
                self.drone.land()
            elif "apple" in command:
                self.drone.takeoff()
            else: 
                print("I don't understand the command")
        except sr.UnknownValueError:
            pass   
     
        # with self.microphone as source:
        #     audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=3)

        # try:
        #     command = self.recognizer.recognize_google(audio).lower()
        #     print(command)

        #     if "land" in command:
        #         self.drone.land()
        #     elif "takeoff" in command:
        #         self.drone.takeoff()
        #     else:
        #         print("I don't understand the command")
        # except sr.UnknownValueError:
        #     pass



