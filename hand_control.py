# Created by Alex Pereira

# Import libraries
import cv2 as cv
import serial

# Import classes
from hands import HandDetector

# Creates the Gesture Class
class Gesture:
    # Constructor
    def __init__(self, capture) -> None:
        # Create the serial device
        # self.arduino = serial.Serial(port = 'COM4', baudrate = 9600)
        
        # Reads capture in init
        self.cap = capture
        self.readCapture()
        print("Camera opened sucessfully!")

        # Creates an instance of HandDetector
        global detector
        detector = HandDetector(maxHands = 2, detectionCon = 0.75, minTrackCon = 0.75)
    
    def readCapture(self):
        """
        Reads the capture.
        """
        # Reads the capture
        success, stream = self.cap.read()

        # If read fails, raise an error
        if not success:
            raise IOError("Camera error! Failed to start!")
        
        return stream

    def liveTracking(self):
        """
        Similar to the old liveTracking() method and to be used for display purposes.
        """
        # Reads the capture
        stream = self.readCapture()

        # Hand detection 2.0
        allHands, stream = detector.findHands(stream)

        # Show the stream
        cv.imshow("MediaPipe Hands", stream)

        return allHands, stream

    def fingerControl(self):
        """
        Moves the finger servos.
        """
        # Track hands
        hands, stream = self.liveTracking()

        # 
        if hands is not None:
            # Hand 1
            if len(hands) >= 1:
                hand1 = hands[0]
                landmarkList1 = hand1["landmarkList"]  # List of 21 Landmark points
                boundingBox1  = hand1["boundingBox"]  # Bounding box info x,y,w,h
                centerPoint1  = hand1['center']  # center of the hand cx,cy
                handType1     = hand1["type"]  # Handtype Left or Right

                fingers1      = detector.fingersUp(hand1)
                print("Hand1 Fingers:", fingers1)
            
            # Hand 2
            if len(hands) >= 2:
                hand2 = hands[1]
                landmarkList2 = hand2["landmarkList"]  # List of 21 Landmark points
                boundingBox2  = hand2["boundingBox"]  # Bounding box info x,y,w,h
                centerPoint2  = hand2['center']  # center of the hand cx,cy
                handType2     = hand2["type"]  # Hand Type "Left" or "Right"

                fingers2      = detector.fingersUp(hand2)
                print("Hand2 Fingers:", fingers2)