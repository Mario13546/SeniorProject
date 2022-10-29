# https://www.youtube.com/watch?v=dbZZlq1_M4o&ab_channel=PaulMcWhorter
import serial

arduino = serial.Serial("COM7", 9600)

while True:
    cmd = input("Type command here: ")
    cmd = cmd + "\r"
    arduino.write(cmd.encode())