import importlib
import logging
from typing import Optional
import click
import os
import json
import re
import sys

import subprocess
from dotenv import load_dotenv
from ..const.globals import COLOR_GRAY_DARK, COLOR_RED, WEX_VERSION, COMMAND_PATTERN, LOG_FILENAME, COLOR_CYAN
from ..const.error import ERR_ARGUMENT_COMMAND_MALFORMED, ERR_COMMAND_FILE_NOT_FOUND, ERR_EXEC_NON_CLICK_METHOD
from pythonjsonlogger import jsonlogger
import importlib.util
from ..core.action.CoreActionsCoreAction import CoreActionsCoreAction
from ..core.action.TestCreateCoreAction import TestCreateCoreAction
from ..core.action.TestCoreAction import TestCoreAction
from ..core.action.HiCoreAction import HiCoreAction
from ..helper.string import camel_to_snake_case


class Kernel:
    addons: [str] = {}
    logger: 'Logger'
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }
    version = WEX_VERSION
    registry: {} = None
    test_manager = None
    core_actions = {
        'core-actions': CoreActionsCoreAction,
        'hi': HiCoreAction,
        'test': TestCoreAction,
        'test-create': TestCreateCoreAction,
    }

    def __init__(self, path_root):
        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(path_root)) + '/'
        self.path['addons'] = self.path['root'] + 'addons/'
        self.path['tmp'] = self.path['root'] + 'tmp/'
        self.path['logs'] = self.path['tmp'] + 'logs/'

        path_registry = self.path['tmp'] + 'registry.json'

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
        with open(self.path['root'] + '/locale/messages.json') as f:
            self.messages = json.load(f)

        # Initialize addons config
        self.addons = {addon: {'config': {}} for addon in self.list_subdirectories(self.path['addons'])}

        for addon in self.addons:
            messages_path = self.path['addons'] + f'{addon}/locale/messages.json'

            if os.path.exists(messages_path):
                with open(messages_path) as file:
                    self.messages.update(json.load(file))

        # Create the log folder if it does not exist
        if not os.path.exists(self.path['logs']):
            os.makedirs(self.path['logs'])

        # Load env
        load_dotenv()

        # Create logger, in json format for better parsing.
        self.logger = logging.getLogger()
        # Add json formatter for logger.
        # Beware: the output file is not a json,
        # but a text file with a json on each line.
        # Parsers should parse it before reading as a json.
        log_handler = logging.FileHandler(self.path['logs'] + LOG_FILENAME)
        formatter = jsonlogger.JsonFormatter('%(asctime)s [%(levelname)s] %(message)s')
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)

    def trans(self, key: str, parameters: object = {}, default=None) -> str:
        message = self.messages.get(key, default or key)

        return message.format(**parameters)

    def error(self, code: str, parameters: object = {}) -> None:
        message = f'[{code}] {self.trans(code, parameters, "Unexpected error")}'

        click.echo(
            click.style(
                message,
                fg=COLOR_RED,
                bold=True
            )
        )

        self.logger.error(message)

        exit(1)

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

    def log_notice(self, message: str) -> None:
        self.log(message, COLOR_CYAN)

    def validate_argv(self, args: []) -> bool:
        if len(args) > 1:
            return True
        return False

    def call(self):
        if not self.validate_argv(sys.argv):
            return

        command: str = sys.argv[1]
        command_args: [] = sys.argv[2:]

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

    def exec(self, command: str, command_args: {}):
        command = camel_to_snake_case(command)

        # Handle core action : test, hi, etc...
        if command in self.core_actions:
            action = command
            command = None
            if command_args:
                command = command_args.pop(0)

            action = self.core_actions[action](self)

            return action.exec(command, command_args)

        # Check command formatting.
        match = re.match(COMMAND_PATTERN, command)
        if not match:
            self.error(ERR_ARGUMENT_COMMAND_MALFORMED)
            return

        # Get valid path.
        command_path: str = self.build_command_path_from_match(match)
        if not os.path.exists(command_path):
            self.error(ERR_COMMAND_FILE_NOT_FOUND, {
                'command': command,
                'path': command_path,
            })
            return

        function = self.get_function_from_match(match)

        addon, group, name = match.groups()

        middleware_args = {
            'addon': addon,
            'args': command_args,
            'command': command,
            'function': function,
            'group': group,
            'name': name,
        }

        self.exec_middlewares('exec', middleware_args)

        result = self.exec_function(function, command_args)

        self.exec_middlewares('exec_post', middleware_args)

        return result

    ctx = None

    def get_group_names(self, addon):
        group_names = set()

        if addon in self.registry['addons']:
            for command in self.registry['addons'][addon]['commands'].keys():
                group_name = command.split("::")[1].split("/")[0]
                group_names.add(group_name)
        return list(group_names)

    def build_command_path_from_command(self, command: str, subdir=None):
        match = re.match(COMMAND_PATTERN, command)
        return self.build_command_path_from_match(match, subdir)

    def build_command_path_from_match(self, match, subdir=None):
        base_path = f"{self.path['addons']}{match.group(1)}/"

        if subdir:
            base_path += f"{subdir}/"

        return f"{base_path}command/{match.group(2)}/{match.group(3)}.py"

    def get_function_from_command(self, command):
        match = re.match(COMMAND_PATTERN, command)
        return self.get_function_from_match(match)

    def get_function_from_match(self, match):
        command_path = self.build_command_path_from_match(match)

        # Import module and load function.
        function_name: str = f'{match.group(1)}_{match.group(2)}_{match.group(3)}'
        spec = importlib.util.spec_from_file_location(command_path, command_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, function_name)

    def env(self, key: str):
        return self.enf[key]

    def convert_dict_to_args(self, function, args):
        """
        Convert args {"arg": "value"} to list ["--arg", "value"].
        """
        arg_list = []
        for param in function.params:
            if param.name in args:
                if isinstance(param, click.Option):
                    arg_list.append(f'--{param.name}')
                arg_list.append(args[param.name])
        return arg_list

    def exec_function(self, function, args=None):
        if args is None:
            args = []

        if not click.get_current_context(True):
            # Lists uses invoke instead of callback.
            if isinstance(args, list):
                ctx = function.make_context('', args)
                ctx.obj = self

                return function.invoke(ctx)
            else:
                ctx = function.make_context('', self.convert_dict_to_args(function, args))
                ctx.obj = self

        if hasattr(function, 'callback'):
            return function.callback(**args)

        self.error(ERR_EXEC_NON_CLICK_METHOD, {
            'function_name': function.__name__
        })

    def list_subdirectories(self, path: str) -> []:
        subdirectories = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                subdirectories.append(os.path.basename(item_path))

        subdirectories.sort()

        return subdirectories

    def shell_exec(self, command: str):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True
        )

        # Display output in real time.
        for line in iter(process.stdout.readline, b''):
            print(line.decode().strip())

        # Get output
        output, error = process.communicate()
        if error:
            print(error.decode())
        else:
            print(output.decode())
