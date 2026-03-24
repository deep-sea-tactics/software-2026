import pygame
import copy #for deep copying the default config to avoid mutating it when creating new Controller instances
import pprint #for complex data structures like dictionaries and lists, this will print them in a more readable format

class Controller:
    def __init__(self, joystick, config_file = None, default_config = None):
        pygame.init()
        pygame.joystick.init()
        screen = pygame.display.set_mode((1, 1))  # 1x1 pixel, basically invisible
        pygame.display.iconify()                  # immediately minimizes it
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
            print("No joysticks connected. Would you like to use keyboard controls instead? (y/n)")
            if input().lower() == 'y':
                print("Keyboard controls enabled.")
                self.controller = None # Set controller to None to indicate we're using keyboard controls
            else:
                print("Exiting program.")
                exit()
    

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





from default_config import default_config

ctrl = Controller(joystick=0, default_config=default_config)

# Assign some bindings
ctrl.config_bindings("Forward",  "Controller", index=0, value=(1, 1))   # axis 1 pushed forward
ctrl.config_bindings("Backward", "Controller", index=0, value=(1, -1))  # axis 1 pushed backward
ctrl.config_bindings("Stop All", "Controller", index=0, value=0)        # button 0
ctrl.config_bindings("Up",       "Controller", index=0, value=(0, (0, 1)))  # hat up
ctrl.config_bindings("Forward",  "Keyboard",   index=0, value="w")
ctrl.config_bindings("Forward",  "Keyboard",   index=1, value="up")

# Main loop
while True:
    ctrl.handle_events()

"""