
# Binding formats:
#   Button:  integer              e.g. 0, 1, 2...
#   Axis:    (axis_num, dir)      e.g. (1, 1) = pushed forward, (1, -1) = pushed backward
#   Hat:     (hat_index, (x, y)) e.g. (0, (0, 1)) = up, (0, (0, -1)) = down
#   Key:     string               e.g. "w", "space", "up"
#
# Each action: [primary, fallback]


default_config = {
    "Controller": {
        "Up":                           [4, None],
        "Down":                         [2, None],
        "Strafe Left":                  [(0,-1), None],
        "Strafe Right":                 [(0,1), None],
        "Forward":                      [(1,1), None],
        "Backward":                     [(1,-1), None],
        "Yaw Left":                     [(2,-1), None],
        "Yaw Right":                    [(2,1), None],
        "Pitch Up":                     [5, None],
        "Pitch Down":                   [3, None],
        "Roll Left":                    [6, None],
        "Roll Right":                   [7, None],
        "Arm Open":                     [(3,1), None],
        "Arm Close":                    [(3,-1), None],
        "Take Photo":                   [0, None],
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