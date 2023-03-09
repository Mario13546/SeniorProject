# Created by Alex Pereira

# Import Libraries
import cv2   as cv
import numpy as np
from   time import sleep

#  Import classes
from ASL                  import Signing
from hands                import HandDetector
from serial_communication import SerialComms

# Creates the Gesture Class
class Gesture:
    def __init__(self, capture, maxHands, detectionCon, minTrackCon) -> None:
        """
        Constructor for the Gestures class.
        @param videoCapture
        @param maxNumberOfHands
        @param minimumDetectionConfidence
        @param minimumTrackingConfidence
        """
        # Creates a serial object
        self.arduino = SerialComms()

        # Reads capture in init
        self.cap = capture
        self.readCapture()
        print("Camera opened sucessfully")

        # Creates an instance of Signing
        self.signing = Signing()

        # Creates an instance of HandDetector
        self.detector = HandDetector(maxHands = maxHands, detectionCon = detectionCon, minTrackCon = minTrackCon)
    
    def readCapture(self):
        """
        Reads the VideoCapture capture.
        @return videoStream
        """
        # Reads the capture
        success, stream = self.cap.read()

        # If read fails, raise an error
        if not success:
            raise OSError("Camera error! Failed to start!")
        
        return stream

    def liveTracking(self):
        """
        Tracks all hands that move across the screen.
        Does NOT cause the prosthetic to move.
        @return allDetectedHands
        """
        # Reads the capture
        stream = self.readCapture()

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
        handPos = self.signing.getLetterPos(char)

        # Sends the position data to the Arduino with special consideration for some letters
        self.arduino.sendData(handPos)

        # Returns the continue signal
        return True