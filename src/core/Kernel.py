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
from ..const.globals import COLOR_GRAY_DARK, COLOR_RED, WEX_VERSION, COMMAND_PATTERN, LOG_FILENAME
from ..const.error import ERR_ARGUMENT_COMMAND_MALFORMED, ERR_COMMAND_FILE_NOT_FOUND, ERR_EXEC_NON_CLICK_METHOD
from pythonjsonlogger import jsonlogger
import importlib.util


class Kernel:
    addons: [str] = []
    logger: 'Logger'
    path: dict[str, Optional[str]] = {
        "root": None,
        "addons": None
    }
    version = WEX_VERSION

    def __init__(self, path_root):
        # Init global vars.
        self.path['root'] = os.path.dirname(os.path.realpath(path_root)) + '/'
        self.path['addons'] = self.path['root'] + 'addons/'
        self.path['tmp'] = self.path['root'] + 'tmp/'
        self.path['logs'] = self.path['tmp'] + 'logs/'

        # Init addons config
        self.addons = {addon: {} for addon in self.list_subdirectories(self.path['addons'])}

        # Create the log folder if it does not exist
        if not os.path.exists(self.path['logs']):
            os.makedirs(self.path['logs'])

        # Load the messages from the JSON file
        with open(self.path['root'] + '/locale/messages.json') as f:
            self.messages = json.load(f)

        # Load env
        load_dotenv()

        # Create logger, in json for better parsing.
        self.logger = logging.getLogger()
        # Add json formatter for logger.
        # Beware : output file is not a json,
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
        message = f'[{code}] {self.trans(code, parameters, "Unexpected error")}';

        click.echo(
            click.style(
                message,
                fg=COLOR_RED,
                bold=True
            )
        )

        self.logger.error(message)

        exit(1)

    def log(self, message: str) -> None:
        click.echo(
            click.style(
                f'{message}',
                fg=COLOR_GRAY_DARK
            )
        )

        self.logger.info(message)

    def validate_argv(self, args: []) -> bool:
        if len(args) > 1:
            return True
        return False

    def command_to_path(self, command: str) -> str:
        """
        Convert addon::group/name to addon/command/group/name.py

        :param command: full command
        :return: file path
        """
        command = command.replace("::", "/");
        parts: [] = command.split('/')
        parts.insert(1, 'command')

        return self.path['addons'] + '/'.join(parts) + ".py"

    def call(self):
        if not self.validate_argv(sys.argv):
            return

        # Init addons
        for addon in self.addons:
            self.exec_middleware(addon, 'call')

        command: str = sys.argv[1]
        command_args: [] = sys.argv[2:]

        result = self.exec(
            command,
            command_args
        )

        if result is not None:
            print(result)

    def exec_middleware(self, addon: str, name: str):
        middleware_enabled_path = self.path['addons'] + f'{addon}/middleware/{name}.py'

        if os.path.exists(middleware_enabled_path):
            function_name = f'{addon}_middleware_{name}'
            spec = importlib.util.spec_from_file_location(name, middleware_enabled_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            enabled_func = getattr(module, function_name, None)

            return enabled_func(self)

    def exec(self, command: str, command_args: []):
        # Check command formatting.
        match = re.match(COMMAND_PATTERN, command)
        if not match:
            self.error(ERR_ARGUMENT_COMMAND_MALFORMED)
            return

        # Get valid path.
        command_path: str = self.command_to_path(command)
        if not os.path.exists(command_path):
            self.error(ERR_COMMAND_FILE_NOT_FOUND)
            return

        # Import module and load function.
        function_name: str = f'{match.group(1)}_{match.group(2)}_{match.group(3)}'
        spec = importlib.util.spec_from_file_location(command_path, command_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        function = getattr(module, function_name)

        return self.exec_function(function, command_args)

    ctx = None

    def env(self, key: str):
        return self.enf[key]

    def exec_function(self, function, args: [] = []):
        if not click.get_current_context(True):
            with function.make_context('', args) as ctx:
                ctx.obj = self
                return function.invoke(ctx)

        if not hasattr(function, 'callback'):
            self.error(ERR_EXEC_NON_CLICK_METHOD, {
                "function_name": function.__name__
            })

        return function.callback(*args)

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
