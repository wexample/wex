import os
import sys
from typing import Optional

from ..core.action.HiCoreAction import HiCoreAction


class Kernel:
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }
    process_id: str = None
    core_actions = {
        'hi': HiCoreAction,
    }

    def __init__(self, entrypoint_path):
        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(entrypoint_path)) + '/'
        self.path['tmp'] = self.path['root'] + 'tmp/'

    def call(self):
        # No arg found except process id
        if not len(sys.argv) > 2:
            return

        self.process_id = sys.argv[1]

        command: str = sys.argv[2]
        command_args: [] = sys.argv[3:]

        print(
            self.exec(
                command,
                command_args
            )
        )

    def exec(self, command: str, command_args=None):
        if command_args is None:
            command_args = []

        # Handle core action : test, hi, etc...
        if command in self.core_actions:
            action = command
            command = None
            if command_args:
                command = command_args.pop(0)

            action = self.core_actions[action](self)

            return action.exec(command, command_args)
