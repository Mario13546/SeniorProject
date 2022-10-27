# Created by Alex Pereira

# Import Libraries
import cv2  as cv

# Import Classes
from hand_control import Gesture
from camera       import USBCamera

# Create a VideoCapture
camera = USBCamera(0)
cap    = camera.getCapture()

# Instance creation
gesture = Gesture(cap, 10, 0.75, 0.75)

# Main loop
while cap.isOpened() == True:
    # gesture.liveTracking()
    gesture.fingerControl()

    # Press q to end the program
    if ( cv.waitKey(1) == ord("q") ):
        print("Process Ended by User")
        cv.destroyAllWindows()
        break