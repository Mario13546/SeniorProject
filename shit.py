# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value

# https://www.google.com/search?q=how+to+transmit+data+from+python+to+an+arduino&oq=how+to+transmit+data+from+python+to+an+arduino&aqs=chrome..69i57.8097j0j1&sourceid=chrome&ie=UTF-8