# Created by Alex Pereira

# Imports
import numpy as np
import cv2   as cv
import serial
import time

# Variables
inp = "90"

# Creates the Serial Class
class Serial:
    # Constructor
    def __init__(self) -> None:
        # Create the serial device
        # self.arduino = serial.Serial('COM4', 9600)
        
        # Variables
        self.testCount = 0

    # Sends a servo position to the Arduino (0 - 179)
    def serialTest(self):
        # Gets user input
        inp = input("Input value of 0 - 179: ")

        # Encodes the input
        encInp = inp.encode()

        # Writes the encoded value to serial
        # self.arduino.write(encInp)
        
        # Increments testCount
        self.testCount += 1

        # Returns the test count
        return self.testCount