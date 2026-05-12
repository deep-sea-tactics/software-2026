from controls.default_config import ACTION_TO_DOF
from controls.default_config import default_config
from controls.controls import Controller
from arm.arm import Arm

import pygame

ctrls = Controller(0, default_config=default_config)
clock = pygame.time.Clock()  # Create a clock object to manage the frame rate
running = True

ArmObj = Arm()

ctrls.bind_action_to_function("Arm Open", lambda: ArmObj.open(ArmObj))
ctrls.bind_action_to_function("Arm Close", lambda: ArmObj.close(ArmObj))

while running:
    print("handling events")
    ctrls.handle_events()
    vec = ctrls.get_input_vector()
    print(vec)  # For testing, print the input vector to see the values being generated when keys are pressed. This should show a 6-element array corresponding to the DOFs based on the key presses.
    clock.tick(10)  # Limit to 30 frames per second 


''' ignore for the moment
import paramiko
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# start server

# start client to RPI using SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(hostname='192.168.0.2', username=os.getenv('rpi_username'), password=os.getenv('rpi_password'))
(stdin, stdout, stderr) = client.exec_command('python3 software-2026/networking/client.py')
stdin.close()
''' 



