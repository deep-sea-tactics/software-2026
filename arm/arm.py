'''
The arm isn't too important a feature but it appears
to be pretty simple to test. So, we can use the arm
to test the general capability of both the input and
networking systems. 
'''

import pigpio
import time

# Establish the necessary PWM signal widths/durations (in microseconds)
ARM_CLOSE_WIDTH = 1600
ARM_NEUTRAL_WIDTH = 1500
ARM_OPEN_WIDTH = 1400

class Arm:
    def __init__(self, pigpio_ip, pigpio_port, arm_signal_pin):
        # Intialize pigpio
        try: 
            self.pi = pigpio.pi(pigpio_ip, pigpio_port)
        except:
            print("Failed to connect to pigpio daemon")
        
        # Initalize arm
        self.pin = arm_signal_pin 
        self.pi.set_mode(self.pin, pigpio.OUTPUT) #listener
        self.pi.set_PWM_frequency(self.pin, 50) # Set frequency to 50Hz 
    
    # Sends PWM signals to close arm
    def close(self):
        print("closing arm")
        self.pi.set_servo_pulsewidth(self.pin, ARM_CLOSE_WIDTH)

    # Sends PWM signals to open arm
    def open(self):
        print("opening arm")
        self.pi.set_servo_pulsewidth(self.pin, ARM_OPEN_WIDTH)

    # Neutral signal
    def stop(self):
        self.pi.set_servo_pulsewidth(self.pin, ARM_NEUTRAL_WIDTH)

if __name__ == "__main__":
    # Testing
    armTest = Arm("192.168.0.2", 8888)
    while True:
        armTest.open()
        time.sleep(2)
        armTest.stop()
        time.sleep(2)
        armTest.close()
        time.sleep(2)