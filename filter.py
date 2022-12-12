# Created by Alex Pereira

# Creates the GestureFilter Class
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

    def runAllFilters(self, fingers):
        """
        Runs all of the filters in this class
        @param fingerPositionArray
        """
        # Makes the parameter local
        fingerPos = fingers

        # Middle finger censor
        fingerPos = self.censorMiddleFinger(fingerPos)

        # Returns the position array
        return fingerPos

    def censorMiddleFinger(self, fingerPos, servoRange = 180):
        """
        Censors the middle finger.
        @param fingerPositionArray
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
            # Adjusts the position array, removing the middle finger
            fingerPos[self.middleId] = 0
        else:
            # Does nothing to the position array
            fingerPos = fingerPos

        # Returns the position array
        return fingerPos