import pygame

pygame.init()

pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

#joystick_count = pygame.joystick.get_count()

