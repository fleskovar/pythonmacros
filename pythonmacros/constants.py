from pynput import keyboard


EDITOR = "editor"
BUTTONS = "buttons"
MACROS = "macros"
KEYS = "keys"
SCRIPT = "script"
OPEN_CONFIG = "open_config"
MACROS_PATH = "macros_path"
EDIT_MODE_TOGGLE = "edit_mode_toggle"
LIB_PATH = "lib_path"
MAP = "map"
RECORD_MODE = "record_mode"

KEY_MAP = {
    "F1": keyboard.Key.f1,
    "F2": keyboard.Key.f2,
    "F3": keyboard.Key.f3,
    "F4": keyboard.Key.f4,
    "F5": keyboard.Key.f5,
    "F6": keyboard.Key.f6,
    "F7": keyboard.Key.f7,
    "F8": keyboard.Key.f8,
    "F9": keyboard.Key.f9,
    "F10": keyboard.Key.f10,
    "F11": keyboard.Key.f11,
    "F12": keyboard.Key.f12,
    "ctrl": keyboard.Key.ctrl,
    "shift": keyboard.Key.shift,
    "alt": keyboard.Key.alt,
}
