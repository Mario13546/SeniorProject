# Created by Alex Pereira

# Import Libraries
import string
import numpy as np

# Creates the Signing Class
class Signing:
    def __init__(self) -> None:
        """
        Constructor for the Signing class.
        """
        # Creates variables related to letters
        self.letters = np.array(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], dtype = str)
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Creates the position arrays
        self.position = np.zeros(self.letters.shape[0]).tolist()

        # Inits the positions
        self.initPositions()

    def initPositions(self):
        """
        Stores positional values in the position array.
        """
        self.position[0]  = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # A
        self.position[1]  = np.array([000, 180, 180, 180, 180, 90], dtype = np.float32)  # B
        self.position[2]  = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # C
        self.position[3]  = np.array([000, 180, 000, 000, 000, 90], dtype = np.float32)  # D
        self.position[4]  = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # E
        self.position[5]  = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # F
        self.position[6]  = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # G
        self.position[7]  = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # H
        self.position[8]  = np.array([000, 000, 000, 000, 180, 90], dtype = np.float32)  # I
        self.position[9]  = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # J
        self.position[10] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # K
        self.position[11] = np.array([180, 180, 000, 000, 000, 90], dtype = np.float32)  # L
        self.position[12] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # M
        self.position[13] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # N
        self.position[14] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # O
        self.position[15] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # P
        self.position[16] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # Q
        self.position[17] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # R
        self.position[18] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # S
        self.position[19] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # T
        self.position[20] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # U
        self.position[21] = np.array([000, 180, 180, 000, 000, 90], dtype = np.float32)  # V
        self.position[22] = np.array([000, 180, 180, 180, 000, 90], dtype = np.float32)  # W
        self.position[23] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # X
        self.position[24] = np.array([180, 000, 000, 000, 180, 90], dtype = np.float32)  # Y
        self.position[25] = np.array([000, 000, 000, 000, 000, 90], dtype = np.float32)  # Z

    def getLetterPos(self, letter: str):
        """
        Returns the position array associated with a letter.
        """
        # Gets the position of a letter
        ind = string.ascii_letters.index(letter)

        # Accounts for uppercase letters
        if (ind >= 26):
            ind -= 26

        return self.position[ind]