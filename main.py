# Created by Alex Pereira

# Import Libraries
from time import sleep

# Import Classes
from hand_control import Gesture

# Instance creation
gesture = Gesture(maxHands = 1, detectionCon = 0.75, minTrackCon = 0.75)

# Test mode setting
test = False

# Add a slight delay
sleep(1)

# Main loop
while (test == False):
    # gesture.liveTracking()
    gesture.liveHandControl()

    # Press q to end the program
    if ( gesture.getEnd() == True ):
        break

# Test loop
while (test == True):
    test = gesture.signLetters()