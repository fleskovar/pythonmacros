from pynput import keyboard
import os
from .editor import open_config_editor
from .config_loader import Config

pressed_keys = set()
edit_mode = False


def get_callbacks(config: Config):
    
    def check_combination(keys, edit_mode_flag):
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
                else:
                    # Edit script
                    open_config_editor(config.editor_path, script)

    def on_press(key):
        global edit_mode
        if key == keyboard.Key.esc:
            # Condition for exiting
            raise KeyboardInterrupt()
        
        config.keep_alive()

        pressed_keys.add(key)
        
        if config.editor_button.issubset(pressed_keys):
            # Open config file in editor
            open_config_editor(config.editor_path, config.config_path)
        elif config.edit_mode_button.issubset(pressed_keys):
            # Toggle edit mode on/off
            edit_mode = not edit_mode
            for edit_key in config.edit_mode_button:
                pressed_keys.remove(edit_key)
        
        print(" " * 100, end="\r")
        print(f"Edit mode: {edit_mode} -    {key}", end="\r")
        
        check_combination(pressed_keys, edit_mode)

    def on_release(key):
        try:
            pressed_keys.remove(key)
        except KeyError:
            # The key may have already been removed (e.g., if two keys were released simultaneously).
            pass

    return on_press, on_release


def start_listener(config: Config):
    press_callback, release_callback = get_callbacks(config)
    with keyboard.Listener(
        on_press=press_callback, on_release=release_callback
    ) as listener:
        listener.join()
        pass
