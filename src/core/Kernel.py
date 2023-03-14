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
from ..const.error import ERR_ARGUMENT_COMMAND_MALFORMED, ERR_COMMAND_FILE_NOT_FOUND
from pythonjsonlogger import jsonlogger


class Kernel:
    version = WEX_VERSION
    logger: 'Logger'
    path: dict[str, Optional[str]] = {
        "root": None,
        "addons": None
    }

    def __init__(self, path_root):
        # Init global vars.
        self.path['root'] = os.path.dirname(os.path.realpath(path_root)) + '/'
        self.path['addons'] = self.path['root'] + 'addons/'
        self.path['tmp'] = self.path['root'] + 'tmp/'

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
        log_handler = logging.FileHandler(self.path['tmp'] + LOG_FILENAME)
        formatter = jsonlogger.JsonFormatter('%(asctime)s [%(levelname)s] %(message)s')
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)

    def trans(self, key: str, parameters: object = {}) -> str:
        return self.messages[key].format(**parameters)

    def error(self, code: str, parameters: object = {}) -> None:
        message = f'[{code}] {self.trans(code, parameters)}';

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

    def path_to_module(self, path: str) -> str:
        relative_path = os.path.relpath(path, self.path['root'])
        module_path, _ = os.path.splitext(relative_path)
        module_path = module_path.replace(os.path.sep, ".")

        return module_path

    def call(self):
        if not self.validate_argv(sys.argv):
            return

        command: str = sys.argv[1]
        command_args: [] = sys.argv[2:]

        self.exec(
            command,
            command_args
        )

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
        module_name: str = self.path_to_module(command_path)
        module: 'ModuleType' = importlib.import_module(module_name)
        function = getattr(module, function_name)

        ctx = function.make_context(command, command_args or [])
        ctx.obj = self
        return function.invoke(ctx)

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
