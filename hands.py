# Created by Alex Pereira

# Import Libraries
import math
import cv2       as cv
import mediapipe as mp

# Import Classes
from filter import GestureFilter

# Creates the HandDetector Class
class HandDetector:
    # Constructor
    def __init__(self, maxHands = 2, modelComplexity = 0, detectionCon = 0.5, minTrackCon = 0.5):
        """
        Constructor for HandDetector.
        @param maxHands
        @param modelComplexity
        @param detectionConfidence
        @param minimumTrackingConfidence
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

        # Creates the variables for length calculations
        self.HandDistance    = 0
        self.maxHandWidth    = 0
        self.fingerDistance  = [0] * 5
        self.maxFingerLength = [0] * 5

        # Creates an instance of GestureFilter
        self.gFilter = GestureFilter()

        # Variables
        self.width, self.height, self.center = 0, 0, 0

    def findHands(self, stream):
        """
        Finds hands in a stream.
        @param stream
        @return allDetectedHands
        @return annotatedStream
        """
        # Creates a blank array
        allHands = []

        # Flips the image
        stream = cv.flip(stream, 1)

        # Converts the image to RGB
        streamRGB = cv.cvtColor(stream, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(streamRGB)
        stream.flags.writeable = False

        # Gets the shape of the image
        self.height, self.width, self.center = stream.shape

        # If the results.multi_hand_landmarks array is not empty
        if self.results.multi_hand_landmarks:
            for handType, handLandmarks in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                # Generates an empty dictionary
                myHand = {}

                # Generates some empty lists
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
                cx, cy = boundingBox[0] + (boundingBox[2] / 2), boundingBox[1] + (boundingBox[3] / 2)

                # Adds the values to myHand
                myHand["landmarkList"] = myLandmarkList
                myHand["boundingBox"]  = boundingBox
                myHand["center"]       = (cx, cy)
                myHand["type"]         = str(handType.classification[0].label)

                # Adds the hand data to allHands[]
                allHands.append(myHand)

                # Draw the Hand landmarks
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

                # Writes the identifier
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

    def getHandPosition(self, myHand):
        """
        Finds how many fingers are open and how rotated the wrist is.
        Considers left and right hands separately.
        @param anyHand
        @return fingerPositionArray
        """
        # Creates a blank array
        fingerPos = []

        # Lets me be lazy with x, y, and z values
        x, y, z, = 0, 1, 2

        # Creates arrays with the entries in the dictionary
        myHandType            = myHand["type"]
        myLandmarkList        = myHand["landmarkList"]
        self.tempLandmarkList = myHand["landmarkList"]  # Avoids having to make the myHand dictionary a self variable

        if self.results.multi_hand_landmarks:
            # Runs the detection only if the hand is oriented in the correct manner
            if (myLandmarkList[self.tipIds[2]][y] < myLandmarkList[0][y]):
                # Thumb
                if myHandType == "Right":
                    # Helps see the thumb correctly even if the palm is back of the hand is facing the camera
                    if (myLandmarkList[self.tipIds[0]][x] > myLandmarkList[self.tipIds[4]][x]):
                        if (myLandmarkList[self.tipIds[0]][x] > myLandmarkList[self.tipIds[0] - 2][x]):
                            fingerPos.append(self.getFingerLength(0))
                        else:
                            fingerPos.append(0)
                    else:
                        if (myLandmarkList[self.tipIds[0]][x] > myLandmarkList[self.tipIds[0] - 2][x]):
                            fingerPos.append(0)
                        else:
                            fingerPos.append(self.getFingerLength(0))
                elif myHandType == "Left":
                    # Helps see the thumb correctly even if the palm is back of the hand is facing the camera
                    if (myLandmarkList[self.tipIds[0]][x] < myLandmarkList[self.tipIds[4]][x]):
                        if (myLandmarkList[self.tipIds[0]][x] < myLandmarkList[self.baseIds[0]][x]):
                            fingerPos.append(self.getFingerLength(0))
                        else:
                            fingerPos.append(0)
                    else:
                        if (myLandmarkList[self.tipIds[0]][x] < myLandmarkList[self.baseIds[0]][x]):
                            fingerPos.append(0)
                        else:
                            fingerPos.append(self.getFingerLength(0))

                # Other 4 fingerPos
                for id in range(1, 5):
                    if (myLandmarkList[self.tipIds[id]][y] < myLandmarkList[self.baseIds[id]][y]):
                        fingerPos.append(self.getFingerLength(id))
                    else: 
                        if (id == 2):
                            # Adjusts the middle finger's zero position to avoid a hardware issue
                            fingerPos.append(10)
                        else:
                            fingerPos.append(0)

                # Wrist rotation
                if ((myLandmarkList[self.tipIds[0]][z] < 0) & (myLandmarkList[self.tipIds[4]][z] > 0)):
                    # If the pinky is behind the thumb
                    fingerPos.append(180)
                else:
                    # Anything else
                    fingerPos.append(self.calcWristRotation())
            else:
                # Sets the fingerPos array to 0
                fingerPos = [0] * 6

        # Filter inappropriate gestures
        fingerPos = self.gFilter.runAllFilters(fingerPos)

        return fingerPos

    def getFingerLength(self, finger, servoRange = 180):
        """
        Calculates the max length of a finger.
        @param fingerInQuestion (0 for thumb, 1 for index, etc.)
        @param servoRange
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
        if (self.fingerDistance[finger] < .25):
            # Returns 0 if the distance is less than 0.25 the max
            return 0
        elif (self.fingerDistance[finger] > .75):
            # Returns 180 if the distance is greater than than 0.75 the max
            return servoRange
        else:
            # Returns the actual value if otherwise
            return int(self.fingerDistance[finger] * servoRange)

    def calcWristRotation(self, servoRange = 180):
        """
        Calculates the rotation of the wrist.
        @param servoRange
        """
        # Calculates the X Distance
        xDist = self.calcLandmarkDist(0, self.baseIds[4], 1)

        # Overwrites the previous value if the new one is larger
        if (xDist > self.maxHandWidth):
            self.maxHandWidth = xDist

        # Calculates the ratio of the base to the tip and the full finger
        self.HandDistance = xDist / self.maxHandWidth

        return 90

        # Determines what to return
        if (self.HandDistance < .20):
            # Returns 0 if the distance is less than 20% the max
            return 0
        elif (self.HandDistance > .80):
            # Returns 180 if the distance is greater than than 80% the max
            return servoRange
        else:
            # Returns the actual value if otherwise
            return int(self.HandDistance * servoRange)

    def calcLandmarkDist(self, id1, id2, mode = 0):
        """
        Caclulates and returns the distance between two landmarks.
        @param id1 (0 through 20)
        @param id2 (0 through 20)
        @param typeOfDistanceCalc (0 for hypotenuse, 1 for X distance, 2 for Y distance)
        """
        # Creates a local landmarkList
        landmarkList = self.tempLandmarkList

        # Gets the position data
        x1 = landmarkList[id1][0]
        y1 = landmarkList[id1][1]
        x2 = landmarkList[id2][0]
        y2 = landmarkList[id2][1]

        # Calculates the distance
        if (mode == 0):
            # True distance
            distance = math.dist((x1, y1), (x2, y2))
        elif (mode == 1):
            # X distance
            distance = math.dist((x1, 0), (x2, 0))
        elif (mode == 2):
            # Y distance
            distance = math.dist((0, y1), (0, y2))
        else:
            distance = 0

        # Returns the distance
        return distance