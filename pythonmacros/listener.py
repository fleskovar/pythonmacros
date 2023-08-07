from pynput import keyboard

from .editor import open_config_editor
from .config_loader import Config

pressed_keys = set()
edit_mode = False


def get_callbacks(config: Config):
    def check_combination(keys, edit_mode):
        for trigger, script in config.trigger_data.items():
            if set(trigger).issubset(keys):
                if edit_mode is False:
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
        elif config.editor_button.issubset(pressed_keys):
            # Open config file in editor
            open_config_editor(config.editor_path, config.config_path)
        elif config.edit_mode_button.issubset(pressed_keys):
            # Toggle edit mode on/off
            edit_mode = not edit_mode

        config.keep_alive()
        pressed_keys.add(key)
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
