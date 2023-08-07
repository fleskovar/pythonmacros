import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict
from .constants import (
    MACROS,
    KEYS,
    SCRIPT,
    KEY_MAP,
    BUTTONS,
    OPEN_CONFIG,
    EDITOR,
    MACROS_PATH,
    EDIT_MODE_TOGGLE,
)


class Config:
    def __init__(self, config_path: Path) -> None:
        self._creation_time = None
        self.trigger_data = dict()
        self.editor_button = None
        self.editor_path = None
        self.macros_path = None
        self._config_dict = dict()

        self.config_path = config_path
        self._parse_config()

    def _parse_config(self):
        self._config_dict = self.get_config_dict(self.config_path)

        self.editor_button = set(
            [KEY_MAP.get(c, c) for c in sorted(self._config_dict[BUTTONS][OPEN_CONFIG])]
        )
        self.edit_mode_button = set(
            [
                KEY_MAP.get(c, c)
                for c in sorted(self._config_dict[BUTTONS][EDIT_MODE_TOGGLE])
            ]
        )

        self.editor_path = Path(self._config_dict[EDITOR])
        self.macros_path = Path(self._config_dict[MACROS_PATH])

        self.parse_triggers()

    def get_config_dict(self, config_path: Path) -> Dict:
        self._creation_time = datetime.now()
        with open(config_path, "r+") as f:
            config_dict = json.loads(f.read())
        return config_dict

    def parse_triggers(self):
        trigger_data = dict()
        for trigger in self._config_dict[MACROS]:
            keys = trigger[KEYS]
            script = trigger[SCRIPT]
            keys = tuple(KEY_MAP.get(k, k) for k in sorted(keys))
            trigger_data[keys] = self.macros_path / script
        self.trigger_data = trigger_data

    @staticmethod
    def load(current_path: Path):
        config_path = current_path / "config.json"
        return Config(config_path)

    def _get_file_modified_time(file, file_path) -> datetime:
        return datetime.fromtimestamp(os.path.getmtime(file_path))

    def keep_alive(self) -> None:
        updated_modified_time = self._get_file_modified_time(self.config_path)

        if self._creation_time < updated_modified_time:
            self._parse_config()
