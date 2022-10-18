# Created by Alex Pereira

# Imports
import numpy as np
import cv2   as cv
import serial
import time

# Creates the Serial Class
class Serial:
    def __init__(self) -> None:
        # Create the serial device
        arduino = serial.Serial('COM4', 9600)