# Created by Alex Pereira

# Import libraries
import cv2 as cv
import time

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

    def handControl(self):
        """
        Writes data to the Arduino to move the finger servos.
        """
        # Track hands
        hands = self.liveTracking()

        # Checks if there are any hands
        if hands is not None:
            # Sends the hand data to the arduino
            for ind, hand in enumerate(hands):
                handPos     = self.detector.getHandPosition(hand)
                valReturned = self.arduino.sendData(handPos)
                print("Hand" + str(ind) + " Fingers:", valReturned)

    def motionTest(self, id):
        """
        Induces motion into the didget with the specified id
        :param id  
        """
        # Reads the caapture to continue the main
        self.readCapture()

        # Creates a blank array
        handPos = [0, 0, 0, 0, 0, 0]

        # Sets the proper value to 180
        handPos[id] = 180
        self.arduino.sendData(handPos)

        # Waits 1 seconds
        time.sleep(1)

        # Sets the proper value to 90
        handPos[id] = 90
        self.arduino.sendData(handPos)

        # Waits 1 seconds
        time.sleep(1)

        # Sets the proper value to 0
        handPos[id] = 0
        self.arduino.sendData(handPos)

        # Waits 1 seconds
        time.sleep(1)

        # Sets the proper value to 90
        handPos[id] = 90
        self.arduino.sendData(handPos)

        # Waits for 1 second
        time.sleep(1)