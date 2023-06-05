import importlib
import importlib.util
import logging
import datetime
import os
import json
import sys
from typing import Optional

from addons.core.command.registry.build import core__registry__build
from ..helper.json import load_json_if_valid
from ..helper.file import list_subdirectories
from ..helper.args import convert_args_to_dict, convert_dict_to_args
from ..helper.command import build_command_match, build_function_name_from_match
from ..const.globals import \
    COLOR_CYAN, \
    FILE_REGISTRY, COLOR_RESET, COLOR_GRAY
from ..const.error import \
    ERR_ARGUMENT_COMMAND_MALFORMED, \
    ERR_COMMAND_FILE_NOT_FOUND, COLORS

from ..core.action.CoreActionsCoreAction import CoreActionsCoreAction
from ..core.action.TestCoreAction import TestCoreAction
from ..core.action.HiCoreAction import HiCoreAction
from ..helper.string import format_ignore_missing


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
        'core-actions': CoreActionsCoreAction,
        'hi': HiCoreAction,
        'test': TestCoreAction,
    }
    http_server = None

    def __init__(self, entrypoint_path, process_id: str = None):
        self.process_id = process_id or f"{os.getpid()}.{datetime.datetime.now().strftime('%s.%f')}"

        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(entrypoint_path)) + '/'
        self.path['addons'] = self.path['root'] + 'addons/'
        self.path['tmp'] = self.path['root'] + 'tmp/'
        self.path['log'] = self.path['tmp'] + 'log/'
        self.path['history'] = os.path.join(self.path['tmp'], 'history.json')
        self.path['templates'] = self.path['root'] + 'src/resources/templates/'

        path_registry = f'{self.path["tmp"]}{FILE_REGISTRY}'

        # Load the messages from the JSON file
        with open(self.path['root'] + 'locale/messages.json') as f:
            self.messages = json.load(f)

        # Initialize addons config
        self.addons = {addon: {'config': {}} for addon in list_subdirectories(self.path['addons'])}

        for addon in self.addons:
            messages_path = self.path['addons'] + f'{addon}/locale/messages.json'

            if os.path.exists(messages_path):
                with open(messages_path) as file:
                    self.messages.update(json.load(file))

        # Load registry if empty.
        if not os.path.exists(path_registry):
            self.exec_function(
                core__registry__build
            )

        with open(path_registry) as f:
            self.registry = json.load(f)

        self.exec_middlewares('init')

    def trans(self, key: str, parameters: object = {}, default=None) -> str:
        return format_ignore_missing(
            self.messages.get(key, default or key),
            parameters
        )

    def error(self, code: str, parameters: object = {}, log_level: int = logging.FATAL) -> None:
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

    def log_indent_up(self) -> None:
        self.log_indent += 1

    def log_indent_down(self) -> None:
        self.log_indent -= 1

    def log(self, message: str, color=COLOR_GRAY, increment: int = 0) -> None:
        print(f'{"  " * (self.log_indent + increment)}{color}{message}{COLOR_RESET}')

    def log_notice(self, message: str) -> None:
        self.log(message, color=COLOR_CYAN)

    def call(self):
        # No arg found except process id
        if not len(sys.argv) > 2:
            return

        command: str = sys.argv[2]
        command_args: [] = sys.argv[3:]

        # Init addons
        self.exec_middlewares('call', {
            'command': command,
            'args': command_args
        })

        result = self.exec(
            command,
            command_args
        )

        if result is not None:
            print(result)

    def exec_middlewares(self, name: str, args=None):
        if args is None:
            args = {}

        # Init addons
        for addon in self.addons:
            self.exec_middleware(addon, name, args)

    def exec_middleware(self, addon: str, name: str, args=None):
        if args is None:
            args = {}

        middleware_enabled_path = self.path['addons'] + f'{addon}/middleware/{name}.py'

        if os.path.exists(middleware_enabled_path):
            function_name = f'{addon}_middleware_{name}'
            spec = importlib.util.spec_from_file_location(name, middleware_enabled_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            function = getattr(module, function_name, None)

            return function(self, **args)

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

        addon, group, name = match.groups()

        middleware_args = {
            'addon': addon,
            'args': convert_args_to_dict(function, command_args),
            'args_list': command_args,
            'command': command,
            'function': function,
            'group': group,
            'name': name,
        }

        self.exec_middlewares('exec', middleware_args)

        result = self.exec_function(function, command_args)

        self.exec_middlewares('exec_post', middleware_args)

        return result

    def get_all_commands(self):
        output = {}

        for addon, addon_data in self.registry['addons'].items():
            for command, command_data in addon_data['commands'].items():
                output[command] = command_data

        return output

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

    def add_to_history(self, data: dict):
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
