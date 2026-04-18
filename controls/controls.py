import pygame
import copy #for deep copying the default config to avoid mutating it when creating new Controller instances
import pprint #for complex data structures like dictionaries and lists, this will print them in a more readable format
import numpy as np
from default_config import ACTION_TO_DOF

class Controller:
    def __init__(self, joystick, config_file = None, default_config = None):
        pygame.init()
        pygame.joystick.init()
        screen = pygame.display.set_mode((1, 1))  # 1x1 pixel, basically invisible
        pygame.display.iconify()    
        self.dof_to_index = {"surge": 0, "sway": 1, "heave": 2, "roll": 3, "pitch": 4, "yaw": 5}              # immediately minimizes it
        if config_file is None:
            self.config = copy.deepcopy(default_config)
        else:
            self.config = copy.deepcopy(config_file) # Load config from file if provided, otherwise use default

        joystick_count = pygame.joystick.get_count()
        if joystick_count > 0:
            self.controller = pygame.joystick.Joystick(joystick)
            self.controller.init()
            num_hats = self.controller.get_numhats()
            num_axis = self.controller.get_numaxes()
            num_buttons = self.controller.get_numbuttons()
            print(f"Joystick Name: {self.controller.get_name()}, Number of hats: {num_hats}, Number of axes: {num_axis}, Number of buttons: {num_buttons}")

        else: 
            print("No joysticks connected. Using keyboard controls.")
            print("Keyboard controls enabled.")
            self.controller = None # Set controller to None to indicate we're using keyboard controls
                
    

    def find_action(self, input_type, input_key):
        # Search through the config for the given input type and key
        for action, bindings in self.config.get(input_type, {}).items(): # for action, bindings in self.config[input_type].items():
            if input_key in bindings:
                return action
        return None
    
    def send_command(self, action, raw_value):
        # TODO: replace print with socket send to RPI
        print(f"[COMMAND] Action: '{action}' | Raw value: {raw_value}")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.JOYBUTTONDOWN:
                print(f" {event.button}")
                action = self.find_action("Controller", event.button)
                if action:
                    print(f"[Button {event.button}] -> '{action}'")
                    self.send_command(action, event.button)
                else:
                    print(f"[Button {event.button}] -> No binding found")


            elif event.type == pygame.JOYHATMOTION:
                print(f" {event.hat} {event.value}")
                input_key = (event.hat, event.value)   # e.g. (0, (0, 1))
                action = self.find_action("Controller", input_key)
                if action:
                    print(f"[Hat {event.hat} {event.value}] -> '{action}'")
                    self.send_command(action, event.value)
                else:
                    print(f"[Hat {event.hat} {event.value}] -> No binding found")


            elif event.type == pygame.JOYAXISMOTION:
                if abs(event.value) > 0.1:
                    print(f" {event.axis} {event.value}")
                    # Convert float to -1, 0, or 1
                    direction = 1 if event.value > 0 else -1
                    input_key = (event.axis, direction)  # e.g. (1, 1)
                    action = self.find_action("Controller", input_key)
                    if action:
                        print(f"[Axis {event.axis} dir {direction}] -> '{action}' | value: {event.value:.2f}")
                        self.send_command(action, event.value)
                    else:
                        print(f"[Axis {event.axis} dir {direction}] -> No binding found")
            

            elif event.type == pygame.KEYDOWN:
                pygame.key.set_repeat(200, 50) # Enable key repeat with a delay of 200ms and interval of 50ms
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                    
                print(f" {pygame.key.name(event.key)}")
                key_name = pygame.key.name(event.key)
                # Check if this key is bound to any action in the config
                action = self.find_action("Keyboard", key_name)
                if action:
                    print(f"[Key '{key_name}'] -> '{action}'")
                    self.send_command(action, key_name)
                else:
                    print(f"[Key '{key_name}'] -> No binding found")
            
            elif event.type in (pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED):
                pygame.joystick.quit()
                pygame.joystick.init()
                if pygame.joystick.get_count() > 0:
                    self.controller = pygame.joystick.Joystick(0)
                    self.controller.init()
                else:
                    self.controller = None


    def get_input_vector(self):
        vec = np.zeros(6)
        if self.controller:
            self._read_gamepad(vec)
        else:
            self._read_keyboard(vec)
        return np.clip(vec, -1.0, 1.0)    # Ensure values are between -1 and 1
    

    
    def _read_gamepad(self, vec):
        
        for axis in range(self.controller.get_numaxes()):
            raw = self.controller.get_axis(axis)
            if abs(raw) < 0.08:  # deadzone
                continue
            direction = 1 if raw > 0 else -1
            input_key = (axis, direction)
            action = self.find_action("Controller", input_key)
            if action and action in ACTION_TO_DOF:
                dof, scale = ACTION_TO_DOF[action]
                vec[self.dof_to_index[dof]] += raw * scale

        for btn in range(self.controller.get_numbuttons()):
            if self.controller.get_button(btn):
                action = self.find_action("Controller", btn)
                if action and action in ACTION_TO_DOF:
                    dof, scale = ACTION_TO_DOF[action]
                    vec[self.dof_to_index[dof]] += scale
        
        for hat in range(self.controller.get_numhats()):
            value = self.controller.get_hat(hat)
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # up, down, right, left
                if value == (0,0):
                    continue
                elif value == direction:
                    input_key = (hat, direction)
                    action = self.find_action("Controller", input_key)
                    if action and action in ACTION_TO_DOF:
                        dof, scale = ACTION_TO_DOF[action]
                        vec[self.dof_to_index[dof]] += scale


    def _read_keyboard(self, vec):
        
        keys = pygame.key.get_pressed()
        
        for key_const, pressed in enumerate(keys):
            if not pressed:
                continue
            key_name = pygame.key.name(key_const)
            action = self.find_action("Keyboard", key_name)
            if action and action in ACTION_TO_DOF:
                dof, scale = ACTION_TO_DOF[action]
                vec[self.dof_to_index[dof]] += scale
            
    
