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