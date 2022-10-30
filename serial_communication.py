# Created by Alex Pereira

# Imports
import serial
import serial.tools.list_ports

# Creates the SerialComms Class
class SerialComms:
    # Constructor
    def __init__(self, portNum = None, baudRate = 9600):
        """
        Constructor for the SerialComms class.
        :param serialPortNumber
        :param baudRate
        """
        # Sets variables
        connected = False

        # Port number not given
        if portNum is None:
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                if "Arduino" in port.description:
                    print(f'{port.description} Connected')
                    self.ser = serial.Serial(port.device, baudRate)
                    connected = True
            if not connected:
                raise OSError("Arduino not found. Enter COM port.")
        # Port number given
        else:
            try:
                self.ser = serial.Serial(portNum, baudRate)
                print("Connected to Serial Device")
            except:
                raise OSError("Failed to connect to Serial Device")

    def sendData(self, data):
        """
        Sends the data over serial.
        :param dataArray
        """
        # Creates a string
        myString = ""

        # Adds the data to myString
        for d in data:
            myString += str(int(d))

        # Adds the terminating character to the end
        myString += "\r"

        # Write data to serial
        self.ser.write(myString.encode())

    def getData(self):
        """
        Gets the data from serial.
        :return recievedData
        """
        # Gets and decodes the data
        data = self.ser.read()
        data = data.decode("utf-8")
        
        # Return the data
        return data