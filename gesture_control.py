# Created by Alex Pereira

# Imports
import numpy as np
import cv2   as cv
import serial_comms
import time

# Creates the Gesture Class
class Gesture:
    # Constructor
    def __init__(self) -> None:
        # Create the serial device
        self.arduino = serial_comms.Serial('COM4', 9600)