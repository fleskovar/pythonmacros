import subprocess
import platform


def open_default_config_editor(file_path):
    try:
        if platform.system() == "Linux":
            subprocess.run(["xdg-open", file_path])
        elif platform.system() == "Windows":
            subprocess.run(["start", "", file_path], shell=True)
        elif platform.system() == "Darwin":
            subprocess.run(["open", file_path])
        else:
            print("Unsupported operating system. Cannot open the file.")
    except FileNotFoundError:
        print("Unable to open the file in the default text editor.")


def open_config_editor(editor_path, file_path):
    if editor_path is None:
        open_default_config_editor(file_path)
    else:
        subprocess.run([editor_path, file_path])
