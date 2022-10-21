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

        return allHands

    def fingerControl(self):
        """
        Moves the finger servos.
        """
        # Track hands
        hands = self.liveTracking()

        # 
        if hands is not None:
            # Hand 1
            if len(hands) == 1:
                hand1 = hands[0]
            elif len(hands) == 2:
                hand2 = hands[1]

    def main():
        cap = cv.VideoCapture(0)
        detector = HandDetector(detectionCon=0.8, maxHands=2)
        while True:
            # Get image frame
            success, img = cap.read()
            img = cv.flip(img, 1)

            # Find the hand and its landmarks
            hands, img = detector.findHands(img)
            
            if hands:
                # Hand 1
                hand1 = hands[0]
                lmList1 = hand1["lmList"]  # List of 21 Landmark points
                bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
                centerPoint1 = hand1['center']  # center of the hand cx,cy
                handType1 = hand1["type"]  # Handtype Left or Right

                fingers1 = detector.fingersUp(hand1)

                if len(hands) == 2:
                    # Hand 2
                    hand2 = hands[1]
                    lmList2 = hand2["lmList"]  # List of 21 Landmark points
                    bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
                    centerPoint2 = hand2['center']  # center of the hand cx,cy
                    handType2 = hand2["type"]  # Hand Type "Left" or "Right"

                    fingers2 = detector.fingersUp(hand2)

                    # Find Distance between two Landmarks. Could be same hand or different hands
                    length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img)  # with draw
                    # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
            # Display
            cv.imshow("Image", img)
            cv.waitKey(1)
