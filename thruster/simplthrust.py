import pigpio
import time

thruster_pins = [1,2,3,4,5,6,7,8]  # Example GPIO pins for 8 thrusters/ESCs
pi = pigpio.pi()

esc_max = 1900  # Max pulse width for ESC (1900 microseconds)
esc_min = 1100  # Min pulse width for ESC (1100 microseconds)
esc_neutral = 1500  # Neutral pulse width for ESC (1500 microseconds)

class Thruster:
    def __init__(self, pin):
        self.pin = pin
        pi.set_mode(self.pin, pigpio.OUTPUT)
        self.set_speed(0)  # Start at neutral
        pi.set_servo_pulsewidth(self.pin, esc_neutral)

    def set_speed(self, speed):
        # Speed should be in range -1.0 to 1.0
        if speed < -1.0 or speed > 1.0:
            raise ValueError("Speed must be between -1.0 and 1.0")
        
        # Map speed to pulse width
        if speed >= 0:
            pulse_width = esc_neutral + int(speed * (esc_max - esc_neutral))
        else:
            pulse_width = esc_neutral + int(speed * (esc_neutral - esc_min))
        
        pi.set_servo_pulsewidth(self.pin, pulse_width)
    
    def stop(self):
        pi.set_servo_pulsewidth(self.pin, esc_neutral)

    def stop_all(self):
        for pin in thruster_pins:
            pi.set_servo_pulsewidth(pin, esc_neutral)
    
    