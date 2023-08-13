from pynput import keyboard, mouse
import pyautogui
import threading
import tempfile
import os
from .editor import open_config_editor
from .config_loader import Config
from .recorder import (
    actions_to_script,
    KEY_PRESS,
    KEY_RELEASE,
    CLICK,
    DOUBLE_CLICK,
    RELEASE,
    SCROLL,
    DRAG,
    CTRL_HOTKEY,
)
import time

pressed_keys = set()
recorded_actions = list()
edit_mode = False
recording = False
last_click_time = time.time()  # To track double clicks
lock = threading.Lock()


def get_callbacks(config: Config, mouse_thread):
    def check_combination(keys, edit_mode_flag):
        global pressed_keys
        processed_keys = list()

        for k in list(keys):
            pk = k
            if hasattr(k, "char"):
                # This is a key or control command
                if k.char is not None:
                    code = ord(k.char)
                    pk = k.char if code > 31 else chr(code + 64)
                    pk = pk.lower()
                else:
                    pk = chr(k.vk).lower()
            else:
                if keyboard.Key.ctrl_l == k or keyboard.Key.ctrl_r == k:
                    pk = keyboard.Key.ctrl

            processed_keys.append(pk)

        processed_keys = set(processed_keys)

        for trigger, script in config.trigger_data.items():
            if set(trigger).issubset(processed_keys):
                if not os.path.exists(script):
                    # Open the file in write mode ('w')
                    with open(script, "w") as file:
                        file.write(
                            "# Python macro"
                        )  # Write some initial content if needed
                    open_config_editor(config.editor_path, script)
                elif edit_mode_flag is False:
                    # Execute
                    with open(script, "r") as f:
                        # Load script at execution time to make sure it is always updated
                        exec(f.read())
                        pressed_keys = set()
                        return
                else:
                    # Edit script
                    open_config_editor(config.editor_path, script)

    def on_press(key):
        global edit_mode
        global recording
        global recorded_actions
        if recording is False:
            if key == keyboard.Key.esc:
                # Condition for exiting
                mouse_thread.stop()
                exit()
                return
            config.keep_alive()
            pressed_keys.add(key)
            if config.editor_button.issubset(pressed_keys):
                # Open config file in editor
                open_config_editor(config.editor_path, config.config_path)
            elif config.recording_button.issubset(pressed_keys):
                # Open config file in editor
                recording = True
                pyautogui.PAUSE = 0.0
                return
            elif config.edit_mode_button.issubset(pressed_keys):
                # Toggle edit mode on/off
                edit_mode = not edit_mode
                for edit_key in config.edit_mode_button:
                    pressed_keys.remove(edit_key)

            check_combination(pressed_keys, edit_mode)

            print(" " * 200, end="\r")
            print(f"Edit mode: {edit_mode} -    {key}", end="\r")
        else:
            if key == keyboard.Key.esc:
                # Condition for exiting
                recording = False
                script = actions_to_script(recorded_actions)
                recorded_actions = list()
                save_script(script, config.editor_path)

            try:
                code = ord(key.char)
                key_str = key.char if code > 31 else chr(code + 64)
            except AttributeError:
                code = 99
                key_str = str(key)

            with lock:
                if code > 31:
                    recorded_actions.append((KEY_PRESS, key_str))
                else:
                    recorded_actions.append((CTRL_HOTKEY, key_str))

    def on_release(key):
        global recorded_actions
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)

        try:
            pressed_keys.remove(key)
            with lock:
                recorded_actions.append((KEY_RELEASE, key_str))
        except KeyError:
            # The key may have already been removed (e.g., if two keys were released simultaneously).
            pass

    return on_press, on_release


def save_script(script_lines, editor_path):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as temp_file:
        for l in script_lines:
            temp_file.write(l)
    temp_file_path = temp_file.name
    open_config_editor(editor_path, temp_file_path)


def on_click(x, y, button, pressed):
    global recording
    global last_click_time
    global recorded_actions

    if pressed and recording:
        with lock:
            click_time = time.time()
            if click_time - last_click_time < 0.3:  # Double click threshold
                recorded_actions.append((DOUBLE_CLICK, x, y))
            else:
                recorded_actions.append((CLICK, x, y))
            last_click_time = click_time
    elif not pressed and recording:
        with lock:
            recorded_actions.append((RELEASE, x, y))


def on_scroll(x, y, dx, dy):
    global recording
    global recorded_actions
    if recording:
        with lock:
            recorded_actions.append((SCROLL, dx, dy))


def on_drag(x, y, dx, dy):
    global recording
    global recorded_actions
    if recording:
        with lock:
            recorded_actions.append((DRAG, x, y, dx, dy))


def start_listener(config: Config):
    mouse_listener = mouse.Listener(
        on_click=on_click, on_scroll=on_scroll, on_drag=on_drag
    )
    mouse_listener.start()
        
    
    press_callback, release_callback = get_callbacks(config, mouse_listener)
    keyboard_listener = keyboard.Listener(
        on_press=press_callback, on_release=release_callback
    )
    keyboard_listener.start()
    keyboard_listener.join()
