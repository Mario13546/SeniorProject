# Created by Alex Pereira

# Import Libraries
import cv2 as cv

# Import Classes
from calibration import Calibrate

# Creates the USBCamera class
class USBCamera:
    """
    Use this class to create a USBCamera.
    """
    def __init__(self, camNum: int, camPath: str = None, resolution: tuple = (0, 0), calibrate: bool = False, dirPath: str = "./") -> None:
        """
        Constructor for the USBCamera class.
        @param camNumber
        @param path: It can be found on Linux by running "find /dev/v4l"
        @param resolution: It should be in a (width, length) format
        @param calibrate: Should the camera be calibrated this camera
        @param dirPath: Should be aquired by running "Path(__file__).absolute().parent.__str__()" in the script calling this method
        """
        # Set camera properties
        self.camNum = camNum

        # Init variables
        self.resolution = resolution

        # Creates a capture
        if (camPath is not None):
            # If camPath is known, use the camPath
            self.cap = cv.VideoCapture(camPath)
        else:
            # camPath is unknown, use the camera number
            self.cap = cv.VideoCapture(self.camNum)
        
        # Resizes the capture
        self.resize(resolution)

        # Calibrates if told to do so
        if (calibrate == True):
            self.calibrateCamera(dirPath)

    def resize(self, cameraRes: tuple):
        """
        Resizes the capture to a given resolution.
        If the specified resolution is too high, resizes to the highest resolution possible.
        @param Camera Resolution
        @return resizedCapture
        """
        # Set the values
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, cameraRes[0])
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, cameraRes[1])
        self.cap.set(cv.CAP_PROP_FPS, 10000)

        # Gets the highest value they go to
        width  = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps    = int(self.cap.get(cv.CAP_PROP_FPS))

        # Set the capture to be MJPG format
        self.cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))

        # Prints telemetry
        print("Resolution:", str(width) + "x" + str(height))
        print("Max FPS:", fps)

    def calibrateCamera(self, dirPath: str):
        """
        Calibrates the camera and gets the calibration parameters.
        @param dirPath: The path of the directory calling this function
        """
        # Instance creation
        self.calibrate = Calibrate(self.cap, self.camNum, 15, dirPath)

        # Get results
        ret, self.camMatrix, self.camdistortion, rvecs, tvecs = self.calibrate.calibrateCamera()

    def undistort(self):
        """
        Undistorts an image using cv.undistort().
        @return undistortedStream
        """
        # Creates a cameraMatrix
        newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(self.camMatrix, self.camdistortion, self.resolution, 1, self.resolution)

        # Undistorts the image
        undistortedStream = cv.undistort(self.getStream(), self.camMatrix, self.camdistortion, None, newCameraMatrix)

        # Crops the image
        x, y, w, h = roi
        undistortedStream = undistortedStream[y:y+h, x:x+w]

        return undistortedStream

    def rectify(self):
        """
        Undistorts an image using cv.remap().
        @return undistortedStream
        """
        # Creates a cameraMatrix
        newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(self.camMatrix, self.camdistortion, self.resolution, 1, self.resolution)

        # Unpacks the ROI data
        x, y, w, h = roi

        # Undistorts the image
        mapx, mapy = cv.initUndistortRectifyMap(self.camMatrix, self.camdistortion, None, newCameraMatrix, (w,h), 5)
        undistortedStream = cv.remap(self.getStream(), mapx, mapy, cv.INTER_LINEAR)

        # Crop the image
        undistortedStream = undistortedStream[y:y+h, x:x+w]

        return undistortedStream

    def getStream(self):
        """
        Gets the stream from this camera's capture.
        @return stream
        """
        # Reads the capture
        __, stream = self.cap.read()

        return stream

    def getUndistortedStream(self, algorithm: int = 1):
        """
        Gets the undistorted stream from this camera's capture.
        @param algorithm: 0 to use cv.undistort, 1 to use cv.remap
        @return undistortedStream
        """
        # Undistorts the stream
        if (algorithm == 0):
            stream = self.undistort()
        elif (algorithm == 1): 
            stream = self.rectify()

        return stream

    def getEnd(self):
        """
        Checks if the program should end.
        @return end
        """
        if (cv.waitKey(1) == ord("q")):
            print("Process Ended by User")
            cv.destroyAllWindows()
            self.cap.release()
            return True
        else:
            return False