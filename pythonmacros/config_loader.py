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
    MAP,
    RECORD_MODE,
    ACTIONS,
    CLI,
    ARGS,
    FILE,
    PATTERN,
)


class Config:
    def __init__(self, config_path: Path) -> None:
        self._creation_time = None
        self.trigger_data = dict()
        self.cli_data = dict()
        self.editor_button = None
        self.recording_button = None
        self.editor_path = None
        self._config_dict = dict()
        self.file_monitor = list()

        self.config_path = config_path
        self._default_macro_path = config_path.parent / "default_macros"

        self._parse_config()

    def _buttons_to_set(self, buttons):
        return set([KEY_MAP.get(c, c) for c in sorted(buttons)])

    def _parse_config(self):
        self._config_dict = self.get_config_dict(self.config_path)

        self.editor_button = self._buttons_to_set(
            self._config_dict[BUTTONS][OPEN_CONFIG]
        )

        self.recording_button = self._buttons_to_set(
            self._config_dict[BUTTONS][RECORD_MODE]
        )

        self.edit_mode_button = self._buttons_to_set(
            self._config_dict[BUTTONS][EDIT_MODE_TOGGLE]
        )

        editor_path = self._config_dict.get(EDITOR, None)

        self.editor_path = Path(editor_path) if editor_path is not None else None
        self.parse_triggers()

    def get_config_dict(self, config_path: Path) -> Dict:
        self._creation_time = datetime.now()
        with open(config_path, "r+") as f:
            config_dict = json.loads(f.read())
        return config_dict

    def parse_triggers(self):
        for actions in self._config_dict[ACTIONS]:
            macros_path = actions.get(LIB_PATH, None)

            if MACROS in actions:
                trigger_data = dict()
                for macros_config in actions[MACROS]:
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

            if CLI in actions:
                cli_data = dict()
                for cli_command in actions[CLI]:
                    args = cli_command[ARGS]
                    script = trigger[SCRIPT]
                    keys = tuple(args)
                    cli_data[keys] = macros_path / script
                self.cli_data = cli_data

            if FILE in actions:
                file_monitor = list()
                for monitor in actions[FILE]:
                    file_monitor.append(
                        {
                            PATTERN: monitor[PATTERN],
                            SCRIPT: macros_path / monitor[SCRIPT],
                        }
                    )
                self.file_monitor = file_monitor

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

    def check_cli(self, args):
        return self.cli_data[tuple(args)]
