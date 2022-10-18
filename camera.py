# Created by Alex Pereira

# Imports
import cv2 as cv

# Variables
HIGH_VALUE = 10000

# Creates the USBCamera Class
class USBCamera:
    def __init__(self, camNum) -> None:
        # Sets camera properties
        self.camNum = camNum

        # Auto Resize
        self.autoResize()
    
    def autoResize(self):
        # Creates a capture
        self.cap = cv.VideoCapture(self.camNum)

        # Set the values too high
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, HIGH_VALUE)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, HIGH_VALUE)
        self.cap.set(cv.CAP_PROP_FPS, HIGH_VALUE)

        # Gets the highest value they go to
        width  = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps    = int(self.cap.get(cv.CAP_PROP_FPS))

        # Set the capture to be MJPG format
        self.cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))

        # Prints telemetry
        print("Max Resolution:", str(width) + "x" + str(height))
        print("Max FPS:", fps)
    
    def getCapture(self):
        # Returns the capture
        return self.cap