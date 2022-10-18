# Created by Alex Pereira

# Import Libraries
import cv2   as cv

# Import Classes
from camera  import USBCamera
from serial  import Serial
from hands   import Hands

# Create a VideoCapture
camera = USBCamera(0)
cap    = camera.getCapture()

# Instance creation
serial = Serial()
hands  = Hands(cap)

# Variables
count = 0

# Main loop
while cap.isOpened() == True:
    # hands.liveTracking()
    count = serial.serialTest()

    # Waits for the q key to be pressed
    if ( cv.waitKey(1) == ord("q") ):
        print("Process Ended by User")
        cap.release()
        break

    # Waits for count to exceed 15
    if (count > 14):
        print("Process ended automatically.", "Count:", count)
        break