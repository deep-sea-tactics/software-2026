from controls import Controller
import pygame
from default_config import default_config


ctrls = Controller(0, default_config=default_config)

# Required for keyboard events to register

clock = pygame.time.Clock()  # Create a clock object to manage the frame rate
running = True
while running:
    ctrls.handle_events()
    vec = ctrls.get_input_vector()
    print(vec)  # For testing, print the input vector to see the values being generated when keys are pressed. This should show a 6-element array corresponding to the DOFs based on the key presses.
    clock.tick(30)  # Limit to 30 frames per second