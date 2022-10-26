# Created by Alex Pereira

# Imports
import time
import serial
import serial.tools.list_ports

class SerialComms:
    # Constructor
    def __init__(self, portNo = None, baudRate = 9600, digits = 1):
        # Sets variables
        self.portNo = portNo
        self.baudRate = baudRate
        self.digits = digits
        connected = False

        # Port number not given
        if self.portNo is None:
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                if "Arduino" in p.description:
                    print(f'{p.description} Connected')
                    self.ser = serial.Serial(p.device)
                    self.ser.baudrate = baudRate
                    connected = True
            if not connected:
                raise IOError("Arduino Not Found. Enter COM Port Number.")
        # Port number given
        else:
            try:
                self.ser = serial.Serial(self.portNo, self.baudRate)
                print("Serial Device Connected")
            except:
                raise IOError("Serial Device Not Connected")
    
    # Sends the data over serial
    def sendData(self, data):
        # Creates some strings
        myString = ""

        # For each entry in the array...
        for d in data:
            myString += str(int(d)).zfill(self.digits)

        # Write data to serial
        self.ser.write(myString.encode())
    
    # Gets the data from serial
    def getData(self):
        # Gets the data
        data = self.ser.read()
        data = data.decode("utf-8")
        # data = data.split()
        
        # Return
        return data
    
    # Test method
    def testServos(self):
        # Send the 1's
        self.sendData([1, 1])
        print(self.getData())
        # time.sleep(1)

        # Send the 0's
        # self.sendData([0, 0, 0, 0, 0])
        # time.sleep(1)