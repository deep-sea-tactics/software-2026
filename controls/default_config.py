
# Binding formats:
#   Button:  integer              e.g. 0, 1, 2...
#   Axis:    (axis_num, dir)      e.g. (1, 1) = pushed forward, (1, -1) = pushed backward
#   Hat:     (hat_index, (x, y)) e.g. (0, (0, 1)) = up, (0, (0, -1)) = down
#   Key:     string               e.g. "w", "space", "up"
#
# Each action: [primary, fallback]


default_config = {
    "Controller": {
        "Up":                           [None, None],
        "Down":                         [None, None],
        "Strafe Left":                  [None, None],
        "Strafe Right":                 [None, None],
        "Forward":                      [None, None],
        "Backward":                     [None, None],
        "Yaw Left":                     [None, None],
        "Yaw Right":                    [None, None],
        "Pitch Up":                     [None, None],
        "Pitch Down":                   [None, None],
        "Roll Left":                    [None, None],
        "Roll Right":                   [None, None],
        "Diagonal Strafe Left Forward": [None, None],
        "Diagonal Strafe Right Forward":[None, None],
        "Arm Open":                     [None, None],
        "Arm Close":                    [None, None],
        "Arm Move Forward":             [None, None],
        "Arm Move Backward":            [None, None],
        "Stop All":                     [None, None],
    },
    "Keyboard": {
        "Up":                           ["space", None],
        "Down":                         ["left shift", None],
        "Strafe Left":                  ["a", None],
        "Strafe Right":                 ["d", None],
        "Forward":                      ["w", None],
        "Backward":                     ["s", None],
        "Yaw Left":                     ["r", None],
        "Yaw Right":                    ["t", None],
        "Pitch Up":                     ["u", None],
        "Pitch Down":                   ["i", None],
        "Roll Left":                    ["j", None],
        "Roll Right":                   ["k", None],
        "Diagonal Strafe Left Forward": ["g", None],
        "Diagonal Strafe Right Forward":["h", None],
        "Arm Open":                     ["f", None],
        "Arm Close":                    ["v", None],
        "Arm Move Forward":             ["b", None],
        "Arm Move Backward":            ["n", None],
        "Stop All":                     ["q", None],
    }
}