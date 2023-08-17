import datetime
import os
import sys

from typing import Optional
from src.helper.command import build_command_match
from src.const.globals import \
    COLOR_RESET, COLOR_GRAY
from src.const.error import \
    ERR_ARGUMENT_COMMAND_MALFORMED


class Kernel:
    messages = None
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }

    def __init__(self, entrypoint_path, process_id: str = None):
        self.process_id = process_id or f"{os.getpid()}.{datetime.datetime.now().strftime('%s.%f')}"

        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(entrypoint_path)) + '/'
        self.path['tmp'] = self.path['root'] + 'tmp/'
        self.path['history'] = os.path.join(self.path['tmp'], 'history.json')

    def trans(self, key: str, parameters: object = {}, default=None) -> str:
        # Performance optimisation
        import json
        from src.helper.string import format_ignore_missing

        # Load the messages from the JSON file
        if self.messages is None:
            with open(self.path['root'] + 'locale/messages.json') as f:
                self.messages = json.load(f)

        return format_ignore_missing(
            self.messages.get(key, default or key),
            parameters
        )

    def error(self, code: str, parameters: object = {}, log_level: int = None) -> None:
        # Performance optimisation
        import logging
        from src.const.error import COLORS

        if log_level is None:
            log_level = logging.FATAL

        message = f'[{code}] {self.trans(code, parameters, "Unexpected error")}'

        self.log(
            message,
            COLORS[log_level],
        )

        self.add_to_history(
            {
                'error': code
            }
        )

        if log_level == logging.FATAL:
            exit(1)

    log_indent: int = 0
    indent_string = '  '

    def log_indent_up(self) -> None:
        self.log_indent += 1

    def log_indent_down(self) -> None:
        self.log_indent -= 1

    def build_indent(self, increment: int = 0) -> str:
        return self.indent_string * (self.log_indent + increment)

    def log(self, message: str, color=COLOR_GRAY, increment: int = 0) -> None:
        self.print(f'{self.build_indent(increment)}{color}{message}{COLOR_RESET}')

    def print(self, message):
        print(message)

    def call(self):
        # No arg found except process id
        if not len(sys.argv) > 2:
            return

        command: str = sys.argv[2]
        command_args: [] = sys.argv[3:]

        result = self.exec(
            command,
            command_args
        )

        if result is not None:
            self.print(result)

        # TODO..

    def build_match_or_fail(self, command: str):
        # Check command formatting.
        match, command_type = build_command_match(
            command
        )

        if not match or not command_type:
            self.error(ERR_ARGUMENT_COMMAND_MALFORMED, {
                'command': command
            })

        return match, command_type

    def exec(self, command: str, command_args=None):
        if command_args is None:
            command_args = []

        # Check command formatting.
        match, command_type = self.build_match_or_fail(
            command
        )

    def add_to_history(self, data: dict):
        import json
        from src.helper.json import load_json_if_valid
        from src.helper.file import set_sudo_user_owner

        max_entries = 100
        history = load_json_if_valid(self.path['history']) or []

        history.append({
            'date': str(datetime.datetime.now()),
            'process_id': self.process_id,
            'data': data,
        })

        # if len(history) > max_entries:
        del history[0:len(history) - max_entries]

        with open(self.path['history'], 'w') as f:
            json.dump(history, f, indent=4)
            set_sudo_user_owner(self.path['history'])
