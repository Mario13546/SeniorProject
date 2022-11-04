# Created by Alex Pereira

# Creates the FingerFilter Class
class GestureFilter:
    def __init__(self) -> None:
        """
        Constructor for the GestureFilter class.
        """
        # Variables
        self.thumbId  = 0
        self.indexId  = 1
        self.middleId = 2
        self.ringId   = 3
        self.pinkyId  = 4

    def checkMiddle(self, fingerPos, servoRange = 180):
        """
        Checks for the middle finger.
        :param theFingerPositionArray
        """
        # Creates variables
        numFingersUp   = 0
        middleFingerUp = False

        # Checks if the middle finger is more than halfway up
        if (fingerPos[self.middleId] > (0.5 * servoRange)):
            middleFingerUp = True

        # Counts how many fingers are more than halfway
        for count in range(self.thumbId, self.pinkyId):
            if (fingerPos[count] > (0.5 * servoRange)):
                numFingersUp += 1
            else:
                numFingersUp += 0
        
        # Censors the finger
        if ((middleFingerUp == True) & (numFingersUp == 1)):
            # Adjusted the position array, removing the finger
            fingerPos[self.middleId] = 0
        else:
            # Does nothing to the position array
            fingerPos = fingerPos
        
        # Returns the position array
        return fingerPos