# Created by Alex Pereira

# Imports
import cv2       as cv
import numpy     as np
import mediapipe as mp

mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing        = mp.solutions.drawing_utils
mp_hands          = mp.solutions.hands

# Template Arrays
right_hand_array_template = np.array([
                            ["Right Wrist", 0, 0], # 0
                            ["Right Thumb CMC", 0, 0], # 1
                            ["Right Thumb MCP", 0, 0], # 2
                            ["Right Thumb IP", 0, 0], # 3
                            ["Right Thumb TIP", 0, 0], # 4
                            ["Right Index CMC", 0, 0], # 5
                            ["Right Index MCP", 0, 0], # 6
                            ["Right Index IP", 0, 0], # 7
                            ["Right Index TIP", 0, 0], # 8
                            ["Right Middle CMC", 0, 0], # 9
                            ["Right Middle MCP", 0, 0], # 10
                            ["Right Middle IP", 0, 0], # 11
                            ["Right Middle TIP", 0, 0], # 12
                            ["Right Ring CMC", 0, 0], # 13
                            ["Right Ring MCP", 0, 0], # 14
                            ["Right Ring IP", 0, 0], # 15
                            ["Right Ring TIP", 0, 0], # 16
                            ["Right Pinky CMC", 0, 0], # 17
                            ["Right Pinky MCP", 0, 0], # 18
                            ["Right Pinky IP", 0, 0], # 19
                            ["Right Pinky TIP", 0, 0]  # 20
                            ])
left_hand_array_template  = np.array([
                            ["Left Wrist", 0, 0], # 0
                            ["Left Thumb CMC", 0, 0], # 1
                            ["Left Thumb MCP", 0, 0], # 2
                            ["Left Thumb IP", 0, 0], # 3
                            ["Left Thumb TIP", 0, 0], # 4
                            ["Left Index CMC", 0, 0], # 5
                            ["Left Index MCP", 0, 0], # 6
                            ["Left Index IP", 0, 0], # 7
                            ["Left Index TIP", 0, 0], # 8
                            ["Left Middle CMC", 0, 0], # 9
                            ["Left Middle MCP", 0, 0], # 10
                            ["Left Middle IP", 0, 0], # 11
                            ["Left Middle TIP", 0, 0], # 12
                            ["Left Ring CMC", 0, 0], # 13
                            ["Left Ring MCP", 0, 0], # 14
                            ["Left Ring IP", 0, 0], # 15
                            ["Left Ring TIP", 0, 0], # 16
                            ["Left Pinky CMC", 0, 0], # 17
                            ["Left Pinky MCP", 0, 0], # 18
                            ["Left Pinky IP", 0, 0], # 19
                            ["Left Pinky TIP", 0, 0]  # 20
                            ])

# Creates the Hands Class
class Hands:
    # Constructor
    def __init__(self, capture) -> None:
        # Creates a local capture
        self.cap = capture

        # Gets the active capture properties
        self.width  = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))

        # Create an instance of Handedness
        self.handedness = Handedness(self.width, self.height)

    # Live track the position of the hands
    def liveTracking(self):
        with mp_hands.Hands(max_num_hands = 2, model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as hands:
            # Reads an open USB Camera
            success, stream = self.cap.read()
            if not success:
                raise IOError("Camera error! Failed to start!")
            
            # Small optimizations before processing
            stream = cv.cvtColor(stream, cv.COLOR_RGB2BGR)
            stream = cv.flip(stream, 1)

            # To improve performance, optionally mark the stream as not writeable to pass by reference
            stream.flags.writeable = False
            results = hands.process(stream)
            handData, handsType = self.handedness.calcHandData(results)

            # Draw the hand annotations on the stream
            stream.flags.writeable = True
            stream = cv.cvtColor(stream, cv.COLOR_BGR2RGB)
            stream = self.drawHandPositions(stream, results)
            stream = self.handedness.drawHandedness(stream, handData, handsType)
            
            # Display the streams
            cv.imshow('Mediapipe Hands', stream)

            x1, y1, x2, y2 = 0, 0, 0, 0

        return x1, y1, x2, y2

    # Draws the keypoints and connects them
    def drawHandPositions(self, stream, results):
        if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                    stream,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        return stream

# Creates the Handedness Class
class Handedness:
    # Constructor
    def __init__(self, width, height) -> None:
        # Gets the active camera properties
        self.width  = width
        self.height = height

        # Creates an instance of ArrayStorage
        self.arrayStorage = ArrayStorage()

    # Calculates hand type and parseable data
    def calcHandData(self, results):
        myHands   = []
        handsType = []
        
        if results.multi_hand_landmarks != None:
            for hand in results.multi_handedness:
                # Add classification data to handsType 
                handType = hand.classification[0].label
                handsType.append(handType)

                # Determines what hands are present in the capture
                self.arrayStorage.calcNeededArrays(handsType)

            for handLandMarks in results.multi_hand_landmarks:
                myHand = []
                
                # Adds entries to the myHand array
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x * self.width), int(landMark.y * self.height)))

                # Adds myHand to myHands
                myHands.append(myHand)

                # Fills the arrays with position data
                self.arrayStorage.fillArray1(myHands)
                self.arrayStorage.fillArray2(myHands)

        return myHands, handsType

    # Draw the handedness on each hand
    def drawHandedness(self, stream, handData, handsType):

        for hand, handType in zip(handData, handsType):
            if (handType == 'Right'):
                handColor = (255, 0, 0)
            if (handType == 'Left'):
                handColor = (0, 0, 255)
            
            for ind in [0, 5, 6, 7, 8]:
                cv.circle(stream, hand[ind], 10, handColor, 5)

        return stream

# Creates the ArrayStorage Class
class ArrayStorage:
    # Constructor
    def __init__(self) -> None:
        # Creates two blank numpy arrays
        self.array1 = np.array([])
        self.array2 = np.array([]) 

    # Calulates needed arrays
    def calcNeededArrays(self, handType):
        if (len(handType) > 0 ):
            if (len(handType) >= 1):
                if (handType[0] == "Right"):
                    self.array1 = right_hand_array_template
                elif (handType[0] == "Left"):
                    self.array1 = left_hand_array_template
                else:
                    raise ValueError("Not a possible value")
            if (len(handType) == 2):
                if (handType[1] == "Right"):
                    self.array2 = right_hand_array_template
                elif (handType[1] == "Left"):
                    self.array2 = left_hand_array_template
                else:
                    raise ValueError("Not a possible value")
        else:
            return

    # Fills the first array with data
    def fillArray1(self, data):
        if (len(self.array1) > 0):
            for i in range(0, len(self.array1)):
                if (len(data) > 0):
                    # This is just to unpack two tuples safely
                    dataLayer1 = data[0]
                    dataLayer2 = dataLayer1[i]
                
                    # Sets the values in the array
                    self.array1[i, 1] = dataLayer2[0]
                    self.array1[i, 2] = dataLayer2[1]
                else:
                    return
        else:
            return

    # Fills the second array with data
    def fillArray2(self, data):
        if (len(self.array2) > 0):
            for j in range(0, len(self.array2)):
                if (len(data) > 1):
                    # This is just to unpack two tuples safely
                    dataLayer1 = data[1]
                    dataLayer2 = dataLayer1[j]

                    # Sets the values in the array
                    self.array1[j, 1] = dataLayer2[0]
                    self.array1[j, 2] = dataLayer2[1]
                else:
                    return
        else:
            return

    # Prints the first array
    def printArray1(self):
        print("Array 1: ", self.array1)

    # Prints the second array
    def printArray2(self):
        print("Array 2: ", self.array2)

    # Returns the first array
    def getArray1(self):
        return self.array1

    # Returns the first array
    def getArray2(self):
        return self.array2