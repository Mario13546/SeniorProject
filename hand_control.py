# Created by Alex Pereira

# Import libraries
import cv2 as cv

#  Import classes
from hands                import HandDetector
from serial_communication import SerialComms

# Creates the Gesture Class
class Gesture:
    def __init__(self, capture, maxHands, detectionCon, minTrackCon, testMode = False) -> None:
        """
        Constructor for the Gestures class.
        @param videoCapture
        @param maxNumberOfHands
        @param minimumDetectionConfidence
        @param minimumTrackingConfidence
        """
        # Creates a serial object
        self.arduino = SerialComms(testMode = testMode)

        # Reads capture in init
        self.cap = capture
        self.readCapture()
        print("Camera opened sucessfully")

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
        Similar to the old liveTracking() method and to be used for display purposes.
        @return allDetectedHands
        """
        # Reads the capture
        stream = self.readCapture()

        # Hand detection 2.0
        allHands, stream = self.detector.findHands(stream)

        # Show the stream
        cv.imshow("MediaPipe Hands", stream)

        return allHands

    def fingerControl(self):
        """
        Writes data to the Arduino to move the finger servos.
        """
        # Track hands
        hands = self.liveTracking()

        # Checks if there are any hands
        if hands is not None:
            # Hand 1
            if len(hands) >= 1:
                hand1 = hands[0]

                fingers1  = self.detector.fingersUp(hand1)
                returned1 = self.arduino.sendData(fingers1)
                # print("Hand1 Fingers:", returned1)

            # Hand 2
            if len(hands) >= 2:
                hand2 = hands[1]

                fingers2  = self.detector.fingersUp(hand2)
                returned2 = self.arduino.sendData(fingers2)
                # print("Hand2 Fingers:", returned2)