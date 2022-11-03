# Created by Alex Pereira

# Imports
import math
import cv2       as cv
import mediapipe as mp

# Creates the HandDetector Class
class HandDetector:
    # Constructor
    def __init__(self, maxHands = 2, modelComplexity = 0, detectionCon = 0.5, minTrackCon = 0.5):
        """
        Constructor for HandDetector.
        :param maxHands
        :param modelComplexity
        :param detectionConfidence
        :param minimumTrackingConfidence
        """
        # Initiaizes the MediaPipe Hands solution
        self.maxHands        = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon    = detectionCon
        self.minTrackCon     = minTrackCon

        self.mp_Hands = mp.solutions.hands
        self.hands = self.mp_Hands.Hands(static_image_mode = False,
                                        max_num_hands = self.maxHands,
                                        min_detection_confidence = self.detectionCon,
                                        min_tracking_confidence = self.minTrackCon)
        
        # Creates the drawing objects
        self.mp_drawing        = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Creates the ID lists
        self.tipIds      = [4, 8, 12, 16, 20]
        self.baseIds     = [1, 5, 9, 13, 17]

        # Creates the finger length arrays
        self.fingerDistance  = [0, 0, 0, 0, 0]
        self.maxFingerLength = [0, 0, 0, 0, 0]

        # Variables
        self.width, self.height, self.center = 0, 0, 0

    def findHands(self, stream):
        """
        Finds hands in a stream.
        :param stream
        :return allDetectedHands
        :return annotatedStream
        """
        allHands = []

        # Flips the image
        stream = cv.flip(stream, 1)

        # Converts the image to RGB
        streamRGB = cv.cvtColor(stream, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(streamRGB)
        stream.flags.writeable = False

        # Gets the shape of the image
        self.height, self.width, self.center = stream.shape
        
        if self.results.multi_hand_landmarks:
            for handType, handLandmarks in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                # Generates a dictionary
                myHand = {}
                
                # Generates some lists
                myLandmarkList = []
                xList          = []
                yList          = []

                # Adds cordinates to the landmarkList
                for ind, landmarkList in enumerate(handLandmarks.landmark):
                    px, py, pz = int(landmarkList.x * self.width), int(landmarkList.y * self.height), int(landmarkList.z * self.width)
                    myLandmarkList.append([px, py, pz, ind])
                    xList.append(px)
                    yList.append(py)

                # Bounding Box
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                boundingBox = xmin, ymin, boxW, boxH
                cx, cy = boundingBox[0] + (boundingBox[2] // 2), boundingBox[1] + (boundingBox[3] // 2)

                # Adds the values to myHand
                myHand["landmarkList"] = myLandmarkList
                myHand["boundingBox"]  = boundingBox
                myHand["center"]       = (cx, cy)
                myHand["type"]         = str(handType.classification[0].label)

                # Adds the hand data to allHands[]
                allHands.append(myHand)

                # Draw the Hand ladmarks
                stream.flags.writeable = True
                self.mp_drawing.draw_landmarks( stream,
                                                handLandmarks,
                                                self.mp_Hands.HAND_CONNECTIONS,
                                                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                                self.mp_drawing_styles.get_default_hand_connections_style())

                # Draw the bounding box
                cv.rectangle(stream, (boundingBox[0] - 20, boundingBox[1] - 20),
                                    (boundingBox[0] + boundingBox[2] + 20, boundingBox[1] + boundingBox[3] + 20),
                                    (255, 0, 255), 2)
                
                # Write the identifier
                cv.putText(stream, myHand["type"], (boundingBox[0] - 30, boundingBox[1] - 30), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
                
                # Draws on corners to the rectangle because they're cool
                colorC    = (0, 255, 0)
                l, t, adj = 30, 5, 20
                xmin, ymin, xmax, ymax = xmin - adj, ymin - adj, xmax + adj, ymax + adj
                cv.line(stream, (xmin, ymax), (xmin + l, ymax), colorC, t) # Bottom Left   (xmin, ymax)
                cv.line(stream, (xmin, ymax), (xmin, ymax - l), colorC, t) # Bottom Left   (xmin, ymax)
                cv.line(stream, (xmax, ymax), (xmax - l, ymax), colorC, t) # Bottom Right  (xmax, ymax)
                cv.line(stream, (xmax, ymax), (xmax, ymax - l), colorC, t) # Bottom Right  (xmax, ymax)
                cv.line(stream, (xmin, ymin), (xmin + l, ymin), colorC, t) # Top Left      (xmin, ymin)
                cv.line(stream, (xmin, ymin), (xmin, ymin + l), colorC, t) # Top Left      (xmin, ymin)
                cv.line(stream, (xmax, ymin), (xmax - l, ymin), colorC, t) # Top Right     (xmax, ymin)
                cv.line(stream, (xmax, ymin), (xmax, ymin + l), colorC, t) # Top Right     (xmax, ymin)

        return allHands, stream

    def fingersUp(self, myHand):
        """
        Finds how many fingers are open and returns a list.
        Considers left and right hands separately.
        :param anyHand
        :return fingerPositionArray
        """

        # Creates a blank array
        fingers = []

        # Creates arrays with the entries in the dictionary
        myHandType            = myHand["type"]
        myLandmarkList        = myHand["landmarkList"]
        self.tempLandmarkList = myHand["landmarkList"]  # Avoids having to make the myHand dictionary a self variable

        if self.results.multi_hand_landmarks:
            # Thumb
            if myHandType == "Right":
                # Helps see the thumb correctly even if the palm is back of the hand is facing the camera
                if (myLandmarkList[self.tipIds[0]][0] > myLandmarkList[self.tipIds[4]][0]):
                    if (myLandmarkList[self.tipIds[0]][0] > myLandmarkList[self.tipIds[0] - 2][0]):
                        fingers.append(self.getFingerLength(0))
                    else:
                        fingers.append(0)
                else:
                    if (myLandmarkList[self.tipIds[0]][0] > myLandmarkList[self.tipIds[0] - 2][0]):
                        fingers.append(0)
                    else:
                        fingers.append(self.getFingerLength(0))
            elif myHandType == "Left":
                # Helps see the thumb correctly even if the palm is back of the hand is facing the camera
                if (myLandmarkList[self.tipIds[0]][0] < myLandmarkList[self.tipIds[4]][0]):
                    if (myLandmarkList[self.tipIds[0]][0] < myLandmarkList[self.baseIds[0]][0]):
                        fingers.append(self.getFingerLength(0))
                    else:
                        fingers.append(0)
                else:
                    if (myLandmarkList[self.tipIds[0]][0] < myLandmarkList[self.baseIds[0]][0]):
                        fingers.append(0)
                    else:
                        fingers.append(self.getFingerLength(0))

            # Other 4 Fingers
            for id in range(1, 5):
                if (myLandmarkList[self.tipIds[id]][1] < myLandmarkList[self.baseIds[id]][1]):
                    fingers.append(self.getFingerLength(id))
                else:
                    fingers.append(0)
        
        return fingers

    def getFingerLength(self, finger, servoRange = 180):
        """
        Calculates the max length of a finger.
        :param fingerInQuestion (0 for thumb, 1 for index, etc.)
        """
        # Creates variables
        total = 0

        # Adds up the different segments
        for i in range(self.baseIds[finger], self.tipIds[finger]):
            total += self.calcLandmarkDist(i, i + 1)
        
        # Overwrites the previous value if the new one is larger
        if (total > self.maxFingerLength[finger]):
            self.maxFingerLength[finger] = total

        # Calculates the base to tip distance
        baseToTip = self.calcLandmarkDist(self.tipIds[finger], self.baseIds[finger])

        # Calculates the ratio of the base to the tip and the full finger
        self.fingerDistance[finger] = baseToTip / self.maxFingerLength[finger]

        # Determines what to return
        if (self.fingerDistance[finger] > .15):
            # Returns the actual value if the distance is greater than 1/10th the max
            return int(self.fingerDistance[finger] * servoRange)
        else:
            # Returns 0 if otherwise
            return 0

    def calcLandmarkDist(self, id1, id2):
        """
        Caclulates and returns the distance between two landmarks.
        :param id1
        :param id2
        """
        # Creates a local landmarkList
        landmarkList = self.tempLandmarkList

        # Gets the position data
        x1 = landmarkList[id1][0]
        y1 = landmarkList[id1][1]
        x2 = landmarkList[id2][0]
        y2 = landmarkList[id2][1]

        # Calculates the distance
        distance = math.dist((x1, y1), (x2, y2))

        # Returns the distance
        return distance