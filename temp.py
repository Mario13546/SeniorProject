# Created by Alex Pereira

# Imports
import mediapipe as mp
import cv2       as cv
import math

class HandDetector:
    # Constructor
    def __init__(self, maxHands = 2, modelComplexity = 0, detectionCon = 0.5, minTrackCon = 0.5):
        # Initiaizes the MediaPipe Hands solution
        self.maxHands        = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon    = detectionCon
        self.minTrackCon     = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode = False,
                                        max_num_hands = self.maxHands,
                                        min_detection_confidence = self.detectionCon,
                                        min_tracking_confidence = self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils

        # Creates the ID lists
        self.tipIds       = [4, 8, 12, 16, 20]
        self.fingers      = []
        self.landmarkList = []

    def findHands(self, img):
        """
        Finds hands in an image.
        """
        allHands = []

        # Flips the image
        img = cv.flip(img, 1)

        # Converts the image to BGR
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        img.flags.writeable = False

        # Gets the shape of the image
        height, width, center = img.shape
        
        if self.results.multi_hand_landmarks:
            for handType, handLandmarks in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                
                # Generate lists
                myLandmarkList = []
                xList        = []
                yList        = []

                # Adds cordinates to the landmarkList
                for id, landmarkList in enumerate(handLandmarks.landmark):
                    px, py, pz = int(landmarkList.x * width), int(landmarkList.y * height), int(landmarkList.z * width)
                    myLandmarkList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                # Bounding Box
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                boundingBox = xmin, ymin, boxW, boxH
                cx, cy = boundingBox[0] + (boundingBox[2] // 2), boundingBox[1] + (boundingBox[3] // 2)

                # Sets the values in myHand
                myHand["landmarkList"] = myLandmarkList
                myHand["boundingBox"]  = boundingBox
                myHand["center"]       = (cx, cy)
                
                # Adds the hand data to allHands[] 
                myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                # Draw
                img.flags.writeable = True
                self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
                cv.rectangle(img, (boundingBox[0] - 20, boundingBox[1] - 20),
                                (boundingBox[0] + boundingBox[2] + 20, boundingBox[1] + boundingBox[3] + 20),
                                (255, 0, 255), 2)
                cv.putText(img, myHand["type"], (boundingBox[0] - 30, boundingBox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 2)
                img = self.drawHandedness(img, myHand["landmarkList"], myHand["type"])
        
        return allHands, img

    def fingersUp(self, myHand):
        """
        Finds how many fingers are open and returns a list.
        Considers left and right hands separately.
        """

        # Creates an array with the entries in the lists
        myHandType     = myHand["type"]
        myLandmarkList = myHand["landmarkList"]

        if self.results.multi_hand_landmarks:
            fingers = []
            # Thumb
            if myHandType == "Right":
                if myLandmarkList[self.tipIds[0]][0] > myLandmarkList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLandmarkList[self.tipIds[0]][0] < myLandmarkList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Other 4 Fingers
            for id in range(1, 5):
                if myLandmarkList[self.tipIds[id]][1] < myLandmarkList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        
        return fingers

    def findDistance(self, point1, point2, img = None):
        """
        Find the distance between two landmarks based on their x/y location.
        """
        # Seperates the point tuples  
        x1, y1 = point1
        x2, y2 = point2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        # Calcuates the distance between the points
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)

        if img is not None:
            cv.circle(img, (x1, y1), 15, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), 15, (255, 0, 255), cv.FILLED)
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)

            return length, info, img
        else:
            return length, info
    
    def drawHandedness(self, stream, handData, handsType):
        """
        Draws the handedness on the image.
        Blue for right and red for left. 
        """
        handColor = (0, 0, 0)
        for hand, handType in zip(handData, handsType):
            if (handType == 'Right'):
                handColor = (255, 0, 0)
            if (handType == 'Left'):
                handColor = (0, 0, 255)
            
            for ind in [0, 5, 6, 7, 8]:
                cv.circle(stream, hand[ind], 10, handColor, 5)

        return stream