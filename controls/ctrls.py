'''
This file is for testing only.
Use main.py to run the actual program. copy the code below to main.py and fine tune as necessary.
'''

import pygame
from controls import Controller
from default_config import default_config

ctrls = Controller(0, default_config=default_config)

running = True

# Required for keyboard events to register
clock = pygame.time.Clock()  # Create a clock object to manage the frame rate

# Test function binding system
ctrls.bind_action_to_function("Arm Open", lambda: print("opening arm"))
ctrls.bind_action_to_function("Arm Close", lambda: print("closing arm"))

# Main loop for testing
if __name__ == "__main__":
    while running:
        ctrls.handle_events()
        vec = ctrls.get_input_vector()
        print(vec)  # For testing, print the input vector to see the values being generated when keys are pressed. This should show a 6-element array corresponding to the DOFs based on the key presses.
        clock.tick(10)  # Limit to 30 frames per second 