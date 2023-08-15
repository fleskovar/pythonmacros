from .listener import start_listener
from .config_loader import Config
from pathlib import Path


def main_loop(args):
    print("Started listening for macros. Use Esc to terminate.")

    current_file_path = Path(__file__).resolve().parent
    print("Running on:", current_file_path)

    config = Config.load(current_file_path)
    start_listener(config, args)
