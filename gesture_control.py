# Created by Alex Pereira

# Imports
import numpy as np
import cv2   as cv
import serial

# This will be removed soon as I would like to use my own code
from cvzone.HandTrackingModule import HandDetector
detector = HandDetector(maxHands = 1, detectionCon = 0.8)

# Creates the Gesture Class
class Gesture:
    # Constructor
    def __init__(self) -> None:
        # Create the serial device
        self.arduino = serial.Serial('COM4', 9600)