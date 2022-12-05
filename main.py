# Created by Alex Pereira

# Import Libraries
import cv2 as cv

# Import Classes
from camera       import USBCamera
from hand_control import Gesture

# Create a VideoCapture
camera = USBCamera(0)
cap    = camera.getCapture()

# Instance creation
gesture = Gesture(cap, 1, 0.75, 0.75, testMode = False)

# Main loop
while (cap.isOpened() == True):
    gesture.handControl()
    # gesture.liveTracking()

    # Press q to end the program
    if ( cv.waitKey(1) == ord("q") ):
        print("Process Ended by User")
        cv.destroyAllWindows()
        cap.release()
        break