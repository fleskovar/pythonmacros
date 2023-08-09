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
    LIB_PATH,
    EDIT_MODE_TOGGLE,
    MAP
)


class Config:
    def __init__(self, config_path: Path) -> None:
        self._creation_time = None
        self.trigger_data = dict()
        self.editor_button = None
        self.editor_path = None
        self._config_dict = dict()

        self.config_path = config_path
        self._default_macro_path = config_path.parent / "default_macros"
        
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

        self.parse_triggers()

    def get_config_dict(self, config_path: Path) -> Dict:
        self._creation_time = datetime.now()
        with open(config_path, "r+") as f:
            config_dict = json.loads(f.read())
        return config_dict

    def parse_triggers(self):
        trigger_data = dict()        
        for macros_config in self._config_dict[MACROS]:
            
            macros_path = macros_config.get(LIB_PATH, None)
            
            if macros_path is not None:
                macros_path = Path(macros_config[LIB_PATH])
            else:
                macros_path = self._default_macro_path
            
            triggers = macros_config[MAP]
            
            for trigger in triggers:
                keys = trigger[KEYS]
                script = trigger[SCRIPT]
                keys = tuple(KEY_MAP.get(k, k.lower()) for k in sorted(keys))
                trigger_data[keys] = macros_path / script
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
