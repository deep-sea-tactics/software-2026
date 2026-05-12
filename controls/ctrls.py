#This file is for testing only.
#Use main.py to run the actual program. copy the code below to main.py and fine tune as necessary.
from controls import Controller
import pygame
from default_config import default_config


ctrls = Controller(0, default_config=default_config)

# Required for keyboard events to register

clock = pygame.time.Clock()  # Create a clock object to manage the frame rate

ctrls.bind_action_to_function("Arm Open", lambda: print("opening arm"))
ctrls.bind_action_to_function("Arm Close", lambda: print("closing arm"))

running = True
while running:
    ctrls.handle_events()
    vec = ctrls.get_input_vector()
    print(vec)  # For testing, print the input vector to see the values being generated when keys are pressed. This should show a 6-element array corresponding to the DOFs based on the key presses.
    clock.tick(10)  # Limit to 30 frames per second 