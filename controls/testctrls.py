import pygame 

pygame.init()
pygame.joystick.init()

# Check for connected joysticks
joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    # Get the first available joystick (index 0)
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init() # Initialize the joystick
    print(f"Joystick Name: {my_joystick.get_name()}")
else:
    print("No joysticks connected.")
    my_joystick = None

if my_joystick:
    num_hats = my_joystick.get_numhats()
    print(f"Number of hats: {num_hats}")


if my_joystick:
    num_buttons = my_joystick.get_numbuttons()
    print(f"Number of buttons: {num_buttons}")

    
if my_joystick:
    num_axes = my_joystick.get_numaxes()
    print(f"Number of axes (analog sticks and triggers): {num_axes}")

system_joystick_count = pygame.joystick.get_count()
print(f"Total joysticks connected to system: {system_joystick_count}")



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Get Button ID
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} pressed on joystick instance {event.instance_id}")
            if event.button == 0:
                pygame.quit()
                running = False

        # Get Hat ID and position
        elif event.type == pygame.JOYHATMOTION:
            print(f"Hat {event.hat} moved on joystick instance {event.instance_id}. Position: {event.value}")

        # Get Axis ID and value (includes triggers as axes on some controllers)
        elif event.type == pygame.JOYAXISMOTION:
            # Add a threshold check as axes always send events
            if abs(event.value) > 0.1:
                 print(f"Axis {event.axis} moved on joystick instance {event.instance_id}. Value: {event.value}")
        