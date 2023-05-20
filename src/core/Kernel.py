import logging
import click
import os
import json
import sys
from typing import Optional

from ..const.globals import \
    COLOR_GRAY_DARK, \
    FILE_REGISTRY

from ..core.action.TestCoreAction import TestCoreAction
from ..core.action.HiCoreAction import HiCoreAction


class Kernel:
    logger: None
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }
    process_id: str = None
    test_manager = None
    core_actions = {
        'hi': HiCoreAction,
        'test': TestCoreAction,
    }

    def __init__(self, entrypoint_path):
        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(entrypoint_path)) + '/'
        self.path['addons'] = self.path['root'] + 'addons/'
        self.path['tmp'] = self.path['root'] + 'tmp/'

        path_registry = f'{self.path["tmp"]}{FILE_REGISTRY}'

        # Load registry from file or initialize it.
        if os.path.exists(path_registry):
            with open(path_registry) as f:
                self.registry = json.load(f)

        else:
            self.registry = {
                'addons': {
                    'core': {
                        'commands': {
                            'core::registry/build': self.path['addons'] + 'core/command/registry/build.py'
                        }
                    },
                    'default': {
                        'commands': {

                        }
                    }
                }
            }

        # Create logger, in json format for better parsing.
        self.logger = logging.getLogger()

    log_indent: int = 0

    def log_indent_up(self) -> None:
        self.log_indent += 1

    def log_indent_down(self) -> None:
        self.log_indent -= 1

    def log(self, message: str, color=COLOR_GRAY_DARK) -> None:
        click.echo(
            click.style(
                f'{"  " * self.log_indent}{message}',
                fg=color
            )
        )

        self.logger.info(message)

    def call(self):
        # No arg found except process id
        if not len(sys.argv) > 2:
            return

        self.process_id = sys.argv[1]

        command: str = sys.argv[2]
        command_args: [] = sys.argv[3:]

        result = self.exec(
            command,
            command_args
        )

        if result is not None:
            print(result)

    def setup_test_manager(self, test_manager):
        self.test_manager = test_manager

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
