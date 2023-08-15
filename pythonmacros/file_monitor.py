import os
import glob
import threading
import time
from .config_loader import Config
from .constants import PATTERN, SCRIPT


class FileMonitorThread(threading.Thread):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.stopped = threading.Event()
        self.file_monitor_data = dict()

    def stop(self):
        self.stopped.set()

    def get_file_info(self, file_path):
        return os.path.getmtime(file_path)

    def get_files(self, patterns):
        files = list()
        for pattern in patterns:
            glob_f = glob.glob(pattern)
            files = files + glob_f
        return files

    def run(self):
        while not self.stopped.is_set():
            for monitor in self.config.file_monitor:
                file_list = self.get_files(monitor[PATTERN])

                for monitor_f in file_list:
                    f_time = self.get_file_info(monitor_f)
                    if monitor_f in self.file_monitor_data:
                        if f_time != self.file_monitor_data[monitor_f]:
                            script = monitor[SCRIPT]
                            with open(script, "r") as f:
                                # Load script at execution time to make sure it is always updated
                                exec(f.read())
                    self.file_monitor_data[monitor_f] = f_time

            time.sleep(0.5)  # Polling interval
