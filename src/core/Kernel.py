import importlib.util
import datetime
import os
import sys
import json

from typing import Optional
from addons.app.const.app import ERR_APP_NOT_FOUND, ERR_SERVICE_NOT_FOUND, ERR_CORE_ACTION_NOT_FOUND
from src.helper.user import get_user_home_data_path
from src.helper.file import list_subdirectories
from src.helper.args import convert_dict_to_args, convert_args_to_dict
from src.helper.command import build_command_match, build_command_path_from_match, build_full_command_from_function, \
    get_function_from_match, build_command_from_function
from src.const.globals import \
    FILE_REGISTRY, COLOR_RESET, COLOR_GRAY, COMMAND_TYPE_APP, COMMAND_TYPE_SERVICE, COMMAND_TYPE_CORE, COLOR_CYAN
from src.const.error import \
    ERR_ARGUMENT_COMMAND_MALFORMED, \
    ERR_COMMAND_FILE_NOT_FOUND


class Kernel:
    addons: [str] = {}
    messages = None
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }
    process_id: str = None
    test_manager = None
    core_actions = None
    http_server = None

    def __init__(self, entrypoint_path, process_id: str = None):
        self.process_id = process_id or f"{os.getpid()}.{datetime.datetime.now().strftime('%s.%f')}"

        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(entrypoint_path)) + '/'
        self.path['addons'] = self.path['root'] + 'addons/'
        self.path['core.cli'] = os.path.join(self.path['root'], 'cli', 'wex')
        self.path['tmp'] = self.path['root'] + 'tmp/'
        self.path['log'] = self.path['tmp'] + 'log/'
        self.path['history'] = os.path.join(self.path['tmp'], 'history.json')
        self.path['templates'] = self.path['root'] + 'src/resources/templates/'

        path_registry = f'{self.path["tmp"]}{FILE_REGISTRY}'

        # Initialize addons config
        self.addons = {addon: {'config': {}, 'path': {}} for addon in list_subdirectories(self.path['addons'])}

        # Load registry if empty
        if not os.path.exists(path_registry):
            from addons.core.command.registry.build import core__registry__build

            self.exec_function(
                core__registry__build
            )

        with open(path_registry) as f:
            self.registry = json.load(f)

        # Add user command dir to path.
        user_data_path = get_user_home_data_path()
        commands_path = os.path.join(user_data_path, 'command')
        if os.path.exists(commands_path) and commands_path not in sys.path:
            sys.path.append(commands_path)

        self.exec_middlewares('init')

    def trans(self, key: str, parameters: object = {}, default=None) -> str:
        # Performance optimisation
        from src.helper.string import format_ignore_missing

        # Load the messages from the JSON file
        if self.messages is None:
            with open(self.path['root'] + 'locale/messages.json') as f:
                self.messages = json.load(f)

                for addon in self.addons:
                    messages_path = self.path['addons'] + f'{addon}/locale/messages.json'

                    if os.path.exists(messages_path):
                        with open(messages_path) as file:
                            self.messages.update(json.load(file))

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

    def message(self, message: str, text: str = None):
        import textwrap

        message = f'{COLOR_CYAN}[wex]{COLOR_RESET} {message}'

        if text:
            message += f'\n{COLOR_GRAY}{textwrap.indent(text, (self.log_indent + 1) * self.indent_string)}\n'

        self.print(message)

    def message_next_command(self, command, args={}, message: str = 'You might want now to execute'):
        return self.message_all_next_commands(
            [
                build_full_command_from_function(
                    command,
                    args
                )
            ],
            message
        )

    def message_all_next_commands(
            self,
            commands,
            message: str = 'You might want now to execute one of the following command'
    ):
        self.message(message + ':')

        output = ''
        for command in commands:
            if not isinstance(command, str):
                command = build_command_from_function(command)

            output += f'{self.build_indent(2)}{COLOR_GRAY}>{COLOR_RESET} {command}\n'

        self.print(output)

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

        # App commands should be run in an app dir or subdir
        if command_type == COMMAND_TYPE_APP:
            if not self.addons['app']['path']['call_app_dir']:
                self.error(ERR_APP_NOT_FOUND, {
                    'command': command,
                    'dir': os.getcwd(),
                })
                return
        # Service should exist
        elif command_type == COMMAND_TYPE_SERVICE:
            if match[1] not in self.registry['services']:
                self.error(ERR_SERVICE_NOT_FOUND, {
                    'command': command,
                    'service': match[1],
                })
                return
        # Run core action.
        elif command_type == COMMAND_TYPE_CORE:
            core_actions = self.get_core_actions()

            # Handle core action : test, hi, etc...
            if command in core_actions:
                action = command
                command = None
                if command_args:
                    command = command_args.pop(0)

                action = core_actions[action](self)

                return action.exec(command, command_args)

            else:
                self.error(ERR_CORE_ACTION_NOT_FOUND, {
                    'command': command,
                })
                return

        # Get valid path.
        command_path: str = build_command_path_from_match(self, match, command_type)
        if not os.path.isfile(command_path):
            self.error(ERR_COMMAND_FILE_NOT_FOUND, {
                'command': command,
                'path': command_path,
            })
            return

        function = get_function_from_match(self, match, command_type)

        if isinstance(command_args, dict):
            command_args = convert_dict_to_args(function, command_args)

        middleware_args = {
            'args': convert_args_to_dict(function, command_args),
            'args_list': command_args,
            'command': command,
            'command_type': command_type,
            'function': function,
            'match': match,
        }

        self.exec_middlewares('exec', middleware_args)

        result = self.exec_function(function, command_args)

        self.exec_middlewares('exec_post', middleware_args)

        return result

    def get_core_actions(self):
        if not self.core_actions:
            from src.core.action.CoreActionsCoreAction import CoreActionsCoreAction
            from src.core.action.TestCoreAction import TestCoreAction
            from src.core.action.HiCoreAction import HiCoreAction

            self.core_actions = {
                CoreActionsCoreAction.command(): CoreActionsCoreAction,
                HiCoreAction.command(): HiCoreAction,
                TestCoreAction.command(): TestCoreAction,
            }

        return self.core_actions

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
