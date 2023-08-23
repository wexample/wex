import datetime
import importlib.util
import json
import os
import sys
from typing import Optional

from src.const.error import \
    ERR_ARGUMENT_COMMAND_MALFORMED, ERR_COMMAND_CONTEXT
from src.const.globals import \
    FILE_REGISTRY, COLOR_RESET, COLOR_GRAY, COLOR_CYAN, COMMAND_TYPE_ADDON
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor
from src.core.command.AddonCommandProcessor import AddonCommandProcessor
from src.core.command.AppCommandProcessor import AppCommandProcessor
from src.core.command.CoreCommandProcessor import CoreCommandProcessor
from src.core.command.ServiceCommandProcessor import ServiceCommandProcessor
from src.core.command.UserCommandProcessor import UserCommandProcessor
from src.helper.args import convert_dict_to_args
from src.helper.file import list_subdirectories


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
    processor_classes = [
        AddonCommandProcessor,
        ServiceCommandProcessor,
        AppCommandProcessor,
        UserCommandProcessor,
        CoreCommandProcessor
    ]
    processors = {class_definition.get_type(class_definition): class_definition for class_definition in
                  processor_classes}

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

        # Initialize addons config
        self.addons = {addon: {'config': {}, 'path': {}} for addon in list_subdirectories(self.path['addons'])}

        self.load_registry()

        self.exec_middlewares('init')

    def load_registry(self):
        path_registry = f'{self.path["tmp"]}{FILE_REGISTRY}'

        # Load registry if empty
        if not os.path.exists(path_registry):
            from addons.core.command.registry.build import core__registry__build

            self.exec_function(
                core__registry__build
            )

        with open(path_registry) as f:
            self.registry = json.load(f)

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

    def message_next_command(self, function_or_command, args: dict = {}, command_type: str = COMMAND_TYPE_ADDON,
                             message: str = 'You might want now to execute'):
        return self.message_all_next_commands(
            [
                self.build_command_processor_by_type(command_type).build_full_command_from_function(
                    function_or_command,
                    args,
                )
            ],
            message
        )

    def build_full_command_from_function(self, function_or_command, args: dict = {},
                                         command_type: str = COMMAND_TYPE_ADDON):
        return self.build_command_processor_by_type(command_type).build_full_command_from_function(
            function_or_command,
            args
        )

    def message_all_next_commands(
            self,
            commands,
            message: str = 'You might want now to execute one of the following command',
    ):
        self.message(message + ':')

        commands = "\n".join(commands)
        self.print(
            f'{self.build_indent(2)}{COLOR_GRAY}>{COLOR_RESET} {commands}\n'
        )

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

    def exec(self, command: str, command_args=None):
        if command_args is None:
            command_args = []

        processor = self.build_command_processor(command, command_args)

        if not processor:
            self.error(ERR_ARGUMENT_COMMAND_MALFORMED, {
                'command': command
            })
            return

        return processor.exec()

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

        try:
            ctx = function.make_context('', args or [])
        except Exception as e:
            import logging

            # Show error message
            self.error(
                ERR_COMMAND_CONTEXT,
                {
                    'function': function.callback.__name__,
                    'error': str(e)
                },
                logging.ERROR
            )

            # Show help
            self.print(
                function.get_help(
                    function.make_context('', [])
                )
            )

            return

        ctx.obj = self

        return function.invoke(ctx)

    def add_to_history(self, data: dict):
        from src.helper.json import load_json_if_valid
        from src.helper.file import set_user_or_sudo_user_owner

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
            set_user_or_sudo_user_owner(self.path['history'])

    def build_command_processor_by_type(self, command_type: str) -> AbstractCommandProcessor | None:
        processor_class = self.processors[command_type]
        processor = processor_class(self)

        return processor

    def build_command_processor(self, command, command_args=None) -> AbstractCommandProcessor | None:
        for processor_name in self.processors:
            processor = self.processors[processor_name](
                self,
                command,
                command_args
            )

            # Regex succeed to match command
            if processor.match:
                return processor

        return None
