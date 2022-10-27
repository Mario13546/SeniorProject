# Created by Alex Pereira

# Imports
import time
import serial
import serial.tools.list_ports

# Creates the SerialComms Class
class SerialComms:
    # Constructor
    def __init__(self, portNum = None, baudRate = 9600, digits = 1):
        # Sets variables
        self.portNum = portNum
        self.baudRate = baudRate
        self.digits = digits
        connected = False

        # Port number not given
        if self.portNum is None:
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                if "Arduino" in p.description:
                    print(f'{p.description} Connected')
                    self.ser = serial.Serial(p.device)
                    self.ser.baudrate = baudRate
                    connected = True
            if not connected:
                raise OSError("Arduino Not Found. Enter COM Port Number.")
        # Port number given
        else:
            try:
                self.ser = serial.Serial(self.portNum, self.baudRate)
                print("Serial Device Connected")
            except:
                raise OSError("Serial Device Not Connected")
    
    # Sends the data over serial
    def sendData(self, data):
        # Creates a string
        myString = ""

        # Adds the data to myString
        for d in data:
            myString += str(int(d))

        # Encodes the string
        encodedString = myString.encode()

        # Write data to serial
        self.ser.write(encodedString)

        return encodedString
    
    # Gets the data from serial
    def getData(self):
        # Gets and decodes the data
        data = self.ser.read()
        data = data.decode("utf-8")
        
        # Return the data
        return data
    
    # Test method
    def testServos(self):
        # Send 1's
        self.sendData([1, 1, 1, 1, 1])
        print(self.getData())
        time.sleep(1)

        # Send 0's
        self.sendData([0, 0, 0, 0, 0])
        print(self.getData())
        time.sleep(1)