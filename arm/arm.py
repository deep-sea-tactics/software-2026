'''
The arm isn't too important a feature but it appears
to be pretty simple to test. So, we can use the arm
to test the general capability of both the input and
networking systems. 
'''

import pigpio
import time

# Configure as necessary
arm_signal_pin = 23

# Establish the necessary PWM signal widths/durations (in microseconds)
arm_close_width = 1600
arm_neutral_width = 1500
arm_open_width = 1400

# Intialize pigpio
pi = pigpio.pi("192.168.0.2", 8888) # Connect to pigpio daemon

class Arm:
    def __init__(self, pin):
        self.pin = pin 
        pi.set_mode(self.pin, pigpio.OUTPUT) #listener
        pi.set_PWM_frequency(self.pin, 50) # Set frequency to 50Hz 
    
    def close(self):
        pi.set_servo_pulsewidth(self.pin, arm_close_width)

    def open(self):
        pi.set_servo_pulsewidth(self.pin, arm_open_width)
    
    def stop(self):
        pi.set_servo_pulsewidth(self.pin, arm_neutral_width)

if __name__ == "__main__":
    # Testing
    armTest = Arm(arm_signal_pin)
    while True:
        armTest.open()
        time.sleep(2)
        armTest.stop()
        time.sleep(2)
        armTest.close()
        time.sleep(2)