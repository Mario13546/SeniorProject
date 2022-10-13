# Created by Alex Pereira

# Imports
from camera         import USBCamera
from hands          import Hands

# Create a VideoCapture
camera = USBCamera(0)
cap    = camera.getCapture()

# Instance creation
hands         = Hands(cap)

# Execution
hands.liveTracking()