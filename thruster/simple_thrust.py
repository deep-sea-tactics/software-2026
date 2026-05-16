import pigpio
import time
import numpy as np
from threading import Thread


# Inputs: [Surge, Sway, Heave, Roll, Pitch, Yaw]
# Outputs: [FL, FR, BL, BR, MFL, MFR, MBL, MBR]

# Angle factor 0.7 is 1/sqrt(2) for 45-degree vectored thrusters
S = 0.707 

# Very brute force impelmentation of amperage limits (according to T200 docs, max amperage is ~23A at full throttle)
ESC_MAX = 1712  # Max pulse width for ESC (1900 microseconds)
ESC_MIN = 1288  # Min pulse width for ESC (1100 microseconds)
ESC_NEUTRAL = 1500  # Neutral pulse width for ESC (1500 microseconds)
AMPERAGE_LIMIT = 25 # Max amperage for thrusters
amperage_limit_per_unit = 10 # Set during initialization 

mixer = np.array([
    [ S,  S,   0,   0,   0,  1], # FL
    [-S,  S,   0,   0,   0, -1], # FR
    [-S, -S,   0,   0,   0,  1], # BL
    [ S, -S,   0,   0,   0, -1], # BR
    [ 0,  0,   1,  -1,   1,  0], # MFL
    [ 0,  0,   1,   1,   1,  0], # MFR
    #[ 0,  0,   1,  -1,  -1,  0], # MBL
    #[ 0,  0,   1,   1,  -1,  0]  # MBR
])
#format for thruster outputs is [FL, FR, BL, BR, MFL, MFR, MBL, MBR]

thruster_pins = []  # Example GPIO pins for 8 thrusters/ESCs

class Thruster:
    '''Class to control thrusters using the mixer and GPIO pins'''
    def __init__(self, pigpio_ip, pigpio_port, mixer, thruster_pins):
        # intialize pigpio
        try: 
            self.pi = pigpio.pi(pigpio_ip, pigpio_port)
        except:
            print("Failed to connect to pigpio daemon")

        # Initialize thruster systems
        self.mixer = mixer
        self.thruster_pins = thruster_pins
        self.amperage_limit_per_unit = AMPERAGE_LIMIT / thruster_pins.__len__() # Amperage limit per thruster
        
        for pin in thruster_pins:
            self.pi.set_servo_pulsewidth(pin, ESC_NEUTRAL)  # Initialize all thrusters to neutral (arming)
            self.pi.set_PWM_frequency(pin, 50) # Set frequency to 50Hz

    def set_thruster(self, input):
        # Input is a 6-element array: [Surge, Sway, Heave, Roll, Pitch, Yaw], each in range [-1, 1]
        # Comes from get_input_vector() func in controls.py, which will be called in the main loop of the program.
        thruster_outputs = np.matmul(self.mixer, input)  # Matrix multiplication to get thruster outputs
        max_value = np.max(np.abs(thruster_outputs))
        if max_value > 1:
            thruster_outputs /= max_value  # Normalize to keep within [-1, 1]
    
        # Change thruster outputs from [-1, 1] to [1200, 1800] microseconds for ESC control
        pwm = (thruster_outputs * 300 + ESC_NEUTRAL).astype(int)  # Scale to ESC pulse width range (1100-1900 microseconds)
        pwm = np.clip(pwm, ESC_MIN, ESC_MAX)  # Ensure PWM values are within ESC limits
        
        for pin in range(len(self.thruster_pins)):
            self.pi.set_servo_pulsewidth(self.thruster_pins[pin], pwm[pin])  # Send PWM signal to thruster
            time.sleep(0.00005)  # Small delay to ensure signal is sent properly

    def stop(self):
         # Set thruster to neutral to stop
         for pin in range(len(self.thruster_pins)):
            self.pi.set_servo_pulsewidth(self.thruster_pins[pin], ESC_NEUTRAL)

'''
class ThrusterSystem:
    # Class to manage multiple thrusters with multithreading
   
    def __init__(self, mixer, thruster_pins):
    # Defines list of SingleThruster objects
        self.thrusters = [SingleThruster(mixer, pin) for pin in thruster_pins]

    def set_thrusters(self, input_vector):
    # sets all thrusters based on the input vector using multithreading for simultaneous control
        threads = []
        for thruster in self.thrusters:
            thread = Thread(target=thruster.set_thruster, args=(input_vector,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()  # Wait for all threads to finish

    def stop_all(self):
    # Stops all thrusters 
        for thruster in self.thrusters:
            thruster.stop()
'''

if __name__ == "__main__":
    thrustsys = Thruster(mixer, [16, 17, 22, 25, 26, 27])
    thrustsys.set_thruster([1, 0, 0, 0, 0, 0])  # Example input vector for surge forward
    time.sleep(5)
    thrustsys.stop()
    print("Thrusters stopped successfully.")