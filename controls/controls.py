import pygame
import copy #for deep copying the default config to avoid mutating it when creating new Controller instances
import pprint #for complex data structures like dictionaries and lists, this will print them in a more readable format

class Controller:
    def __init__(self, joystick, config_file = None, default_config = None):
        pygame.init()
        pygame.joystick.init()
        if config_file is None:
            self.config = copy.deepcopy(default_config)
        else:
            self.config = copy.deepcopy(config_file) # Load config from file if provided, otherwise use default

        joystick_count = pygame.joystick.get_count()
        if joystick_count > 0:
            self.controller = pygame.joystick.Joystick(joystick)
            self.controller.init()
            num_hats = self.controller.get_numhats()
            num_axis = self.controller.get_numaxis()
            num_buttons = self.controller.get_numbuttons()
            print(f"Joystick Name: {self.config_bindingscontroller.get_name()}, Number of hats: {num_hats}, Number of axes: {num_axis}, Number of buttons: {num_buttons}")

        else: 
            print("No joysticks connected. Would you like to use keyboard controls instead? (y/n)")
            if input().lower() == 'y':
                print("Keyboard controls enabled.")
                self.controller = None # Set controller to None to indicate we're using keyboard controls
            else:
                print("Exiting program.")
                exit()
    
    def handle_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f" {event.button}")
            
            elif event.type == pygame.JOYHATMOTION:
                print(f" {event.hat} {event.value}")

            elif event.type == pygame.JOYAXISMOTION:
                if abs(event.value) > 0.1:
                    print(f" {event.axis} {event.value}")
            
            elif event.type == pygame.KEYDOWN:
                print(f" {pygame.key.name(event.key)}")
            
    
    def config_bindings(self, action_name, input_type, index, value = None):

        # Validate index — only 0 (primary) or 1 (fallback) allowed
        if index not in (0, 1):
            print(f"[Error] Index must be 0 (primary) or 1 (fallback), got '{index}'")
            return False

        # Check input_type exists
        if input_type not in self.config:
            print(f"[Error] Input type '{input_type}' not found. "
                  f"Available: {list(self.config.keys())}")
            return False

        # Check action_name exists under that input type
        if action_name not in self.config[input_type]:
            print(f"[Error] Action '{action_name}' not found under '{input_type}'. "
                  f"Available: {list(self.config[input_type].keys())}")
            return False

        # Apply the new binding at the correct slot
        self.config[input_type][action_name][index] = value

        slot = "primary" if index == 0 else "fallback"
        print(f"[OK] '{input_type}' > '{action_name}' [{slot}] set to '{value}'")
        return True



    def save_bindings(self, filepath):
        # This function will read the config file and set up the control bindings accordingly
        try:
            with open(filepath, "w") as f:
                f.write("# Auto-generated bindings — do not edit manually\n\n")
                f.write("custom_config = ")
                f.write(pprint.pformat(self.config, indent=4))
                f.write("\n")
            print(f"[OK] Bindings saved to '{filepath}'")
        except IOError as e:
            print(f"[Error] Could not save bindings: {e}")


"""
USE CASE EXAMPLE:

from default_config import default_config

controller = Controller(joystick=0, default_config=default_config)

controller.config_bindings("Up", "Keyboard", 0, "W") # Set primary binding for "Up" action on Controller to Button 0
controller.config_bindings("Up", "Keyboard", 1, "ArrowUp") # Set fallback binding for "Up" action on Controller to Button 1

# Controller with fallback
ctrl.config_bindings("Forward", "Controller", index=0, value="LeftStickUp")
ctrl.config_bindings("Forward", "Controller", index=1, value="DPadUp")

controller.save_bindings("custom_config.py") # Save the current config to a file



"""