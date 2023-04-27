# Created by Alex Pereira

# Import Libraries
import cv2   as cv
import numpy as np
from   time  import sleep

# Import classes
from ASL                  import Signing
from hands                import HandDetector
from camera               import USBCamera
from pathlib              import Path
from serial_communication import SerialComms

# Creates the Gesture Class
class Gesture:
    def __init__(self, maxHands, detectionCon, minTrackCon) -> None:
        """
        Constructor for the Gestures class.
        @param videoCapture
        @param maxNumberOfHands
        @param minimumDetectionConfidence
        @param minimumTrackingConfidence
        """
        # Gets the file path
        filePath = Path(__file__).absolute().parent.__str__()

        # Creates a serial object
        self.arduino = SerialComms()

        # Creates an instance of Signing
        self.signing = Signing()

        # Creates an instance of USBCamera
        self.camera = USBCamera(0, None, (1280, 720), True, filePath)

        # Creates an instance of HandDetector
        self.detector = HandDetector(maxHands = maxHands, detectionCon = detectionCon, minTrackCon = minTrackCon)

    def liveTracking(self):
        """
        Tracks all hands that move across the screen.
        Does NOT cause the prosthetic to move.
        @return allDetectedHands
        """
        # Reads the capture
        stream = self.camera.getUndistortedStream()

        # Hand detection
        allHands, stream = self.detector.findHands(stream)

        # Shows the stream
        cv.imshow("MediaPipe Hands", stream)

        return allHands

    def liveHandControl(self):
        """
        Writes data to the Arduino to move the finger servos.
        """
        # Track hands
        hands = self.liveTracking()

        # Checks if there are any hands
        if (hands is not None):
            # Sends the hand data to the arduino
            for ind, hand in enumerate(hands):
                handPos     = self.detector.getHandPosition(hand)
                valReturned = self.arduino.sendData(handPos)
                print("Hand" + str(ind) + " Fingers:", valReturned)

    def signLetters(self):
        """
        Displays certain letters using American Sign Language, to the best of the machine's ability.
        @return continue
        """
        # Allows the user to input data
        inp  = input("Letter to display: ")
        char = inp[0]

        # Returns the end signal
        if (inp.lower() == "end"):
            return False

        # Creates an array of zeros
        handPos = np.zeros(6)
        handPos[5] = 90  # Makes the wrist stay in the middle

        # Gets the position associated with the letter
        endPos  = self.signing.getLetterPos(char) # The unmodified value
        handPos = self.signing.getLetterPos(char) # The value to account for hardware limitations

        # Sends the position data to the Arduino with special consideration for some letters
        if (char.lower() == "s"):
            handPos = np.array([180] * 6)
            handPos[5] = 90
            self.arduino.sendData(handPos)
            sleep(1)
            handPos = np.array([0] * 6)
            handPos[0] = 180
            handPos[5] = 90
            self.arduino.sendData(handPos)
            sleep(1)
            self.arduino.sendData(endPos)
        elif (char.lower() == "t"):
            handPos = np.array([180] * 6)
            handPos[0] = 0
            handPos[5] = 90
            self.arduino.sendData(handPos)
            sleep(1)
            self.arduino.sendData(endPos)
        else:
            # Prevents the thumb or index finger from getting blocked by the other
            if ((handPos[0] == 0 and handPos[1] != 0) or (handPos[0] != 0 and handPos[1] == 0)):
                handPos[0] = 180
                handPos[1] = 180
                self.arduino.sendData(handPos)
                sleep(1)
                self.arduino.sendData(endPos)
            else:
                # Sends the position data to the Arduino
                self.arduino.sendData(endPos)

        # Returns the continue signal
        return True

    def getEnd(self):
        """
        Gets if the function should end.
        @return end
        """
        return self.camera.getEnd()