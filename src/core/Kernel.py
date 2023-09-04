import datetime
import importlib.util
import json
import os
import sys
import yaml
from typing import Optional

from yaml import SafeLoader

from addons.app.AppAddonManager import AppAddonManager
from src.core.CommandRequest import CommandRequest
from src.core.AddonManager import AddonManager
from src.const.error import \
    ERR_ARGUMENT_COMMAND_MALFORMED, ERR_UNEXPECTED
from src.const.globals import \
    FILE_REGISTRY, COLOR_RESET, COLOR_GRAY, COLOR_CYAN, COMMAND_TYPE_ADDON, KERNEL_RENDER_MODE_CLI
from src.core.command.AbstractCommandResolver import AbstractCommandResolver
from src.core.command.AddonCommandResolver import AddonCommandResolver
from src.core.command.AppCommandResolver import AppCommandResolver
from src.core.command.ServiceCommandResolver import ServiceCommandResolver
from src.core.command.UserCommandResolver import UserCommandResolver
from src.helper.file import list_subdirectories, remove_file_if_exists

PROCESSOR_CLASSES = [
    AddonCommandResolver,
    ServiceCommandResolver,
    AppCommandResolver,
    UserCommandResolver,
]

ADDONS_DEFINITIONS = {
    'app': AppAddonManager
}


class Kernel:
    messages = None
    task_id: str = None
    registry: dict[str, Optional[str]] = {}
    http_server = None
    log_indent: int = 1
    indent_string = '  '
    test = False
    current_request = None

    def __init__(self, entrypoint_path):
        self.post_exec = []

        # Initialize global variables.
        root_path = os.path.dirname(os.path.realpath(entrypoint_path)) + os.sep
        tmp_path = os.path.join(root_path, 'tmp') + os.sep

        self.path = {
            'root': root_path,
            'addons': os.path.join(root_path, 'addons') + os.sep,
            'core.cli': os.path.join(root_path, 'cli', 'wex'),
            'tmp': tmp_path,
            'log': os.path.join(tmp_path, 'log') + os.sep,
            'history': os.path.join(tmp_path, 'history.json'),
            'templates': os.path.join(root_path, 'src', 'resources', 'templates') + os.sep
        }

        # Create a registry for faster access
        self.resolvers = {
            class_definition.get_type(): class_definition
            for class_definition in PROCESSOR_CLASSES
        }

        # Initialize addons config
        self.addons = {}
        for name in list_subdirectories(self.path['addons']):
            definition = ADDONS_DEFINITIONS.get(name, AddonManager)
            self.addons[name] = definition(self, name)

        self.store_task_id()
        self.load_registry()
        self.exec_middlewares('init')

    def load_registry(self):
        path_registry = f'{self.path["tmp"]}{FILE_REGISTRY}'

        # Load registry if empty
        if not os.path.exists(path_registry):
            self.rebuild()

        with open(path_registry) as f:
            self.registry = yaml.load(f, SafeLoader)

    def rebuild(self):
        from addons.core.command.registry.build import core__registry__build

        self.run_function(
            core__registry__build,
            {
                'test': self.test
            }
        )

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

        self.add_to_history(
            {
                'error': code
            }
        )

        if log_level == logging.FATAL:
            from src.core.FatalError import FatalError

            raise FatalError(f'{COLORS[log_level]}{message}{COLOR_RESET}')

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
                self.get_command_resolver(command_type).build_full_command_from_function(
                    function_or_command,
                    args,
                )
            ],
            message
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
        """
        Main entrypoint from bash call.
        May never be called by an internal script.
        :return:
        """
        # No arg found except process id
        if not len(sys.argv) > 2:
            return

        command: str = sys.argv[2]
        command_args: [] = sys.argv[3:]

        result = self.run_command(
            command,
            command_args
        )

        if result is not None:
            self.print(result)

    def run_command(self, command: str, args: dict | list = None, quiet: bool = False):
        request = self.create_command_request(command, args)

        if not request and not quiet:
            self.error(ERR_ARGUMENT_COMMAND_MALFORMED, {
                'command': command
            })

        request.quiet = quiet

        return self.render_response(
            request.run())

    def run_function(self, function, args: dict | list = None, type: str = COMMAND_TYPE_ADDON, quiet: bool = False):
        resolver = self.get_command_resolver(type)

        request = self.create_command_request(
            resolver.build_command_from_function(function),
            args
        )

        request.quiet = quiet

        return self.render_response(
            request.run())

    def render_response(self, response):
        output = response.render(KERNEL_RENDER_MODE_CLI)

        # Store command to execute after kernel execution,
        # it should be set at the last moment,
        # to avoid execution if any error happened before
        for command in self.post_exec:
            from src.helper.command import command_to_string

            self.task_file_write(
                'post-exec',
                command_to_string(command) + '\n',
            )

        return output

    def task_file_path(self, type: str):
        task_dir = os.path.join(self.path['tmp'], 'task')
        os.makedirs(task_dir, exist_ok=True)
        return os.path.join(task_dir, f"{self.task_id}.{type}")

    def task_file_load(self, type: str):
        file_path = self.task_file_path(type)

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        else:
            return None

    def task_file_write(self, type: str, body: str):
        with open(self.task_file_path(type), 'a') as f:
            f.write(body)

    def guess_command_type(self, command: str) -> str | None:
        for type in self.resolvers:
            if self.resolvers[type].supports(self, command):
                return type

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

    def add_to_history(self, data: dict):
        from src.helper.json import load_json_if_valid
        from src.helper.file import set_user_or_sudo_user_owner

        max_entries = 100
        history = load_json_if_valid(self.path['history']) or []

        history.append({
            'date': str(datetime.datetime.now()),
            'task_id': self.task_id,
            'data': data,
        })

        # if len(history) > max_entries:
        del history[0:len(history) - max_entries]

        with open(self.path['history'], 'w') as f:
            json.dump(history, f, indent=4)
            set_user_or_sudo_user_owner(self.path['history'])

    def get_command_resolver(self, type: str) -> AbstractCommandResolver | None:
        if type not in self.resolvers:
            return None
        return self.resolvers[type](self)

    def create_command_request(self, command: str, args: dict | list = None) -> CommandRequest | None:
        resolver = self.get_command_resolver(
            self.guess_command_type(command)
        )

        if resolver:
            return resolver.create_command_request(command, args)

        return None

    def store_task_id(self):
        task_id = sys.argv[1] if len(sys.argv) > 1 else None
        if task_id is None:
            self.error(
                ERR_UNEXPECTED,
                {
                    'error': 'Please use the "bash ./cli/wex" file to run wex script.'
                }
            )
            sys.exit(1)

        self.task_id = sys.argv[1]

        for i, arg in enumerate(sys.argv):
            # There is a redirection
            if arg == '--kernel-task-id' and i + 1 < len(sys.argv):
                task_id = sys.argv[i + 1]

                del sys.argv[i:i + 2]

                self.task_file_write(
                    'task-redirect',
                    task_id
                )

                self.task_id = task_id

                # Cleanup task files to avoid loops.
                remove_file_if_exists(
                    self.task_file_path('post-exec')
                )
