import machine
import time

# Define the servo pin (change to your specific GPIO pin)
SERVO_PIN = 15

# Initialize PWM on the specified pin
# Frequency for servos is typically 50 Hz
pwm = machine.PWM(machine.Pin(SERVO_PIN), freq=50)

def set_servo_angle(angle):
    # Calculate the duty cycle for the angle (standard servos use pulse widths from 1ms to 2ms)
    # The value range for duty cycle on ESP32 PWM is 0-1023
    # This calculation might need adjustment based on your specific servo and ESP32 model
    # A common formula for 50Hz is: duty_cycle = int((angle / 180) * 100 + 25)
    duty_cycle = int((angle * (115 - 35) / 180 + 35) / 1000 * 1023) # Example calc, adjust as needed

    pwm.duty(duty_cycle)

# Loop to sweep the servo from 0 to 180 degrees
while True:
    for angle in range(0, 180, 1):
        set_servo_angle(angle)
        time.sleep_ms(20)
    for angle in range(180, 0, -1):
        set_servo_angle(angle)
        time.sleep_ms(20)
