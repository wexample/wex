import importlib
import importlib.util
import logging
import click
import os
import json
import sys
from typing import Optional

from ..helper.file import list_subdirectories
from ..helper.args import convert_args_to_dict, convert_dict_to_args
from ..helper.command import build_command_match, build_function_name_from_match
from ..const.globals import \
    COLOR_GRAY_DARK, \
    COLOR_RED, \
    FILE_REGISTRY
from ..const.error import \
    ERR_ARGUMENT_COMMAND_MALFORMED, \
    ERR_COMMAND_FILE_NOT_FOUND

from ..core.action.TestCoreAction import TestCoreAction
from ..core.action.HiCoreAction import HiCoreAction
from ..helper.string import to_snake_case, format_ignore_missing


class Kernel:
    addons: [str] = {}
    logger: None
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }
    process_id: str = None
    test_manager = None
    messages = None
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

        # Load the messages from the JSON file
        with open(self.path['root'] + 'locale/messages.json') as f:
            self.messages = json.load(f)

        # Initialize addons config
        self.addons = {addon: {'config': {}} for addon in list_subdirectories(self.path['addons'])}

        # Create logger, in json format for better parsing.
        self.logger = logging.getLogger()

    def trans(self, key: str, parameters: object = {}, default=None) -> str:
        return format_ignore_missing(
            self.messages.get(key, default or key),
            parameters
        )

    def error(self, code: str, parameters: object = {}, log_level: int = logging.FATAL) -> None:
        message = f'[{code}] {self.trans(code, parameters, "Unexpected error")}'

        click.echo(
            click.style(
                message,
                fg=COLOR_RED,
                bold=True
            )
        )

        if log_level == logging.FATAL:
            exit(1)

    log_indent: int = 0

    def log_indent_up(self) -> None:
        self.log_indent += 1

    def log_indent_down(self) -> None:
        self.log_indent -= 1

    def log(self, message: str, color=COLOR_GRAY_DARK, increment: int = 0) -> None:
        click.echo(
            click.style(
                f'{"  " * (self.log_indent + increment)}{message}',
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

    def build_match_or_fail(self, command: str):
        # Check command formatting.
        match = build_command_match(
            command
        )

        if not match:
            self.error(ERR_ARGUMENT_COMMAND_MALFORMED, {
                'command': command
            })

        return match

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

        # Check command formatting.
        match = self.build_match_or_fail(
            command
        )

        # Get valid path.
        command_path: str = self.build_command_path_from_match(match)
        if not os.path.exists(command_path):
            self.error(ERR_COMMAND_FILE_NOT_FOUND, {
                'command': command,
                'path': command_path,
            })
            return

        function = self.get_function_from_match(match)

        if isinstance(command_args, dict):
            command_args = convert_dict_to_args(function, command_args)

        result = self.exec_function(function, command_args)

        return result

    def build_command_path_from_match(self, match, subdir=None):
        base_path = f"{self.path['addons']}{match.group(1)}/"

        if subdir:
            base_path += f"{subdir}/"

        return f"{base_path}command/{match.group(2)}/{match.group(3)}.py"

    def get_function_from_match(self, match):
        command_path = self.build_command_path_from_match(match)

        # Import module and load function.
        spec = importlib.util.spec_from_file_location(command_path, command_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(
            module,
            build_function_name_from_match(match)
        )

    def exec_function(self, function, args=None):
        if not args:
            args = []

        # Enforce sudo.
        if hasattr(function.callback, 'as_sudo') and os.geteuid() != 0:
            os.execvp('sudo', ['sudo'] + sys.argv)

        if isinstance(args, dict):
            args = convert_dict_to_args(function, args)

        ctx = function.make_context('', args or [])
        ctx.obj = self

        return function.invoke(ctx)
