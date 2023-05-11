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
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def fly_drones_voice(self):
        with self.microphone as source:
            audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=3)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(command)

            if "land" in command:
                self.drone.land()
            elif "takeoff" in command:
                self.drone.takeoff()
            else:
                print("I don't understand the command")
        except sr.UnknownValueError:
            pass



