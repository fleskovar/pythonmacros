import threading
from pynput import keyboard
import subprocess
import platform

from .config_loader import Config

pressed_keys = set()
    
        
def get_callbacks(config: Config):

    def check_combination(keys):
        for trigger, script in config.trigger_data.items():
            
            if set(trigger).issubset(keys):
                exec(script)

    def open_default_config_editor():
        file_path = config.config_path
        try:
            if platform.system() == "Linux":
                subprocess.run(['xdg-open', file_path])
            elif platform.system() == "Windows":
                subprocess.run(['start', '', file_path], shell=True)
            elif platform.system() == "Darwin":
                subprocess.run(['open', file_path])
            else:
                print("Unsupported operating system. Cannot open the file.")
        except FileNotFoundError:
            print("Unable to open the file in the default text editor.")


    def open_config_editor():
        if config.editor_path is None:
            open_default_config_editor()
        else:
            subprocess.run([config.editor_path, config.config_path])

    
    def on_press(key):
        if key == keyboard.Key.esc:
            raise KeyboardInterrupt()
        elif key == config.editor_button:
            open_config_editor()
        
        config.keep_alive()
        pressed_keys.add(key)
        check_combination(pressed_keys)

        
    def on_release(key):
        try:
            pressed_keys.remove(key)
        except KeyError:
            # The key may have already been removed (e.g., if two keys were released simultaneously).
            pass
        
    return on_press, on_release
        
def start_listener(config: Config):    
        
    press_callback, release_callback = get_callbacks(config)
    with keyboard.Listener(on_press=press_callback, on_release=release_callback) as listener:
        listener.join()
        pass
