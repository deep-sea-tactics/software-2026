
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
        "Arm Open":                     [None, None],
        "Arm Close":                    [None, None],
        "Take Photo":                   [None, None],
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
        "Arm Open":                     ["f", None],
        "Arm Close":                    ["v", None],
        "Stop All":                     ["q", None],
        "Take Photo":                   ["return", None],
    }
}

ACTION_TO_DOF = {
    "Forward":        ("surge",  1.0),
    "Backward":       ("surge", -1.0),
    "Strafe Left":    ("sway",  -1.0),
    "Strafe Right":   ("sway",   1.0),
    "Up":             ("heave",  1.0),
    "Down":           ("heave", -1.0),
    "Roll Left":      ("roll",  -1.0),
    "Roll Right":     ("roll",   1.0),
    "Pitch Up":       ("pitch",  1.0),
    "Pitch Down":     ("pitch", -1.0),
    "Yaw Left":       ("yaw",   -1.0),
    "Yaw Right":      ("yaw",    1.0),
}