import serial 
from time import sleep

arduino = serial.Serial('COM3', 115200, timeout=0.5)
sleep(5) # Wait for connection

angles = [0, 15, 30, 45, 60 ] 


for angle in angles:
    command = str(angle) 
    arduino.write(command.encode())
sleep(1) 

arduino.close()
