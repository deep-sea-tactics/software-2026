import pygame

pygame.init()

pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

#joystick_count = pygame.joystick.get_count()

class Controller:
    def __init__(self):
        self.joystick = None
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.init()
            print(f"Joystick initialized: {self.joystick.get_name()}")
        else:
            print("No joystick found")

    def get_axis(self, axis):
        if self.joystick:
            return self.joystick.get_axis(axis)
        return 0.0

    def get_button(self, button):
        if self.joystick:
            return self.joystick.get_button(button)
        return False
    

class ROVController:
    def __init__(self):
        self.controller = Controller()
    
    def initialize():
        pygame.init()
        pygame.joystick.init()
    
    def get_controller():
        if pygame.joystick.get_count() > 0:
            print("Controller detected")
        else:
            print("No controller detected")
            exit()
    
    def enumerate_controllers():
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            print(f"Controller {i}: {joystick.get_name()}")
    
    def get_axis(self, axis):
        if self.controller:
            return self.controller.get_axis(axis)
        return 0.0
    
    def get_button(self, button):
        if self.controller:
            return self.controller.get_button(button)
        return False
    
    def button_keybinds(self):
        # Define keybinds for ROV control
        if self.get_button(0):  # Example: Button A for forward
            print("Move Forward")
        if self.get_button(1):  # Example: Button B for backward
            print("Move Backward")
        if self.get_button(2):  # Example: Button X for left
            print("Move Left")
        if self.get_button(3):  # Example: Button Y for right
            print("Move Right")
    
    def axis_keybinds(self):
        # Define keybinds for ROV control based on axis input
        x_axis = -self.get_axis(0)  # Example: Left stick horizontal
        y_axis = -self.get_axis(1)  # Example: Left stick vertical
        
        if y_axis < 0.5:
            print("Move Forward")
        elif y_axis > -0.5:
            print("Move Backward")
        
        if x_axis < 0.5:
            print("Move Left")
        elif x_axis > -0.5:
            print("Move Right")
    
    def quit(self):
        pygame.quit()


import time

ROVController.initialize()
ROVController.get_controller()
ROVController.enumerate_controllers()
rov = ROVController()
while True:
    rov.button_keybinds()
    rov.axis_keybinds()
    time.sleep(0.5)  # Adjust the sleep time as needed