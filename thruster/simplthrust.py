import pigpio
import time
import numpy as np


# Inputs: [Surge, Sway, Heave, Roll, Pitch, Yaw]
# Outputs: [FL, FR, BL, BR, MFL, MFR, MBL, MBR]

# Angle factor 0.7 is 1/sqrt(2) for 45-degree vectored thrusters
s = 0.707 

mixer = np.array([
    [ s,  s,   0,   0,   0,  1], # FL
    [-s,  s,   0,   0,   0, -1], # FR
    [-s, -s,   0,   0,   0,  1], # BL
    [ s, -s,   0,   0,   0, -1], # BR
    [ 0,  0,   1,  -1,   1,  0], # MFL
    [ 0,  0,   1,   1,   1,  0], # MFR
    [ 0,  0,   1,  -1,  -1,  0], # MBL
    [ 0,  0,   1,   1,  -1,  0]  # MBR
])

#format for thruster outputs is [FL, FR, BL, BR, MFL, MFR, MBL, MBR]
thruster_pins = [1,2,3,4,5,6,7,8]  # Example GPIO pins for 8 thrusters/ESCs
pi = pigpio.pi("192.168.0.2", 8888) # Connect to pigpio daemon


esc_max = 1800  # Max pulse width for ESC (1900 microseconds)
esc_min = 1100  # Min pulse width for ESC (1100 microseconds)
esc_neutral = 1500  # Neutral pulse width for ESC (1500 microseconds)

class ThrusterController:
    def __init__(self, mixer, thruster_pins):
        self.mixer = mixer
        self.thruster_pins = thruster_pins
        self.num_thrusters = len(thruster_pins)
        for pin in thruster_pins:
            pi.set_servo_pulsewidth(pin, esc_neutral)  # Initialize all thrusters to neutral (arming)
            pi.set_PWM_frequency(pin, 50) # Set frequency to 50Hz

    #input will be a 6 element array: [Surge, Sway, Heave, Roll, Pitch, Yaw], each in range [-1, 1]
    #that will come from get_input_vector() func in controls.py, which will be called in the main loop of the program.
    def set_thrusters(self, input):
        # input is a 6-element array: [Surge, Sway, Heave, Roll, Pitch, Yaw]
        # Each element should be in the range [-1, 1]
        thruster_outputs = np.matmul(self.mixer, input)  # Matrix multiplication to get thruster outputs
        max_value = np.max(np.abs(thruster_outputs))
        if max_value > 1:
            thruster_outputs/= max_value  # Normalize to keep within [-1, 1]

        #change thruster outputs from [-1, 1] to [1100, 1900] microseconds for ESC control
        pwm = (thruster_outputs * 400 + esc_neutral).astype(int)  # Scale to ESC pulse width range (1100-1900 microseconds)
    
        for i in range(self.num_thrusters):
            print(self.thruster_pins[i])
            pi.set_servo_pulsewidth(self.thruster_pins[i], pwm[i])  # Send PWM signal to each thruster
    
    def stop_all(self):
        for pin in self.thruster_pins:
            pi.set_servo_pulsewidth(pin, esc_neutral)  # Set all thrusters to neutral to stop

# Testing
if __name__ == "__main__":
    thrusterTest = ThrusterController(mixer, [6])
    for i in range(10):
        print("testing thrusters...")
        # Full forward surge
        input_vector = [1, 0, 0, 0, 0, 0]  
        thrusterTest.set_thrusters(input_vector)
        time.sleep(1)
    thrusterTest.stop_all()
