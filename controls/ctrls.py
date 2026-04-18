from controls import Controller
import pygame
from default_config import default_config


ctrls = Controller(0, default_config=default_config)

# Required for keyboard events to register

running = True
while running:
    ctrls.handle_events()
    vec = ctrls.get_input_vector()
    print(vec)  # For testing, print the input vector to see the values being generated when keys are pressed. This should show a 6-element array corresponding to the DOFs based on the key presses.
    