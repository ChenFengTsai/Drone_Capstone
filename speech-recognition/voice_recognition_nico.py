from djitellopy import Tello
import cv2
import numpy as np
import concurrent.futures
import speech_recognition as sr

def fly_drones_voice_3(drone1):
    r = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                print("Timeout reached, listening again...")
                continue

        try:
            command = r.recognize_google(audio).lower()
            print("Recognized speech:", command)  # Added print statement to display recognized speech

            if "end" in command:
                break
            elif "rotate" in command:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    flip_rotate1 = executor.submit(drone1.rotate_clockwise, 360)
                    flip_rotate1.result()
            elif "land" in command:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    take_land1 = executor.submit(drone1.land)
                    take_land1.result()
        except sr.UnknownValueError:
            continue

drone1 = Tello('192.168.87.74')gjnegrjnejgrnjenrg
drone1.connect()
drone1.streamon()
drone1.takeoff()
fly_drones_voice_3(drone1)
