# Created by Alex Pereira

# Import Libraries
from hashlib import new
import cv2   as cv

# Import Classes
from camera import USBCamera
from hands  import Hands

from temp import HandDetector

import cvzone.HandTrackingModule as hd

# Create a VideoCapture
camera = USBCamera(0)
cap    = camera.getCapture()

# Instance creation
hands  = Hands(cap)
det = HandDetector()

# Main loop
while cap.isOpened() == True:
    success, stream = cap.read()
    if not success:
        raise IOError("Camera error! Failed to start!")
        break

    det.findHands(stream)
    # hands.liveTracking()

    # Display the streams
    cv.imshow('Mediapipe Hands', stream)

    # Waits for the q key to be pressed
    if ( cv.waitKey(1) == ord("q") ):
        print("Process Ended by User")
        cap.release()
        break