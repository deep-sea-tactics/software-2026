from controls import Controller
import pygame
from default_config import default_config

ctrls = Controller(0, default_config=default_config)

# Required for keyboard events to register

running = True
while running:
    ctrls.handle_events()