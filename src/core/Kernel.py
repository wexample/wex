import importlib
from typing import Optional
import click
import os
import json
import re
import sys
from ..const.globals import WEX_VERSION, COMMAND_PATTERN
from ..const.error import ERR_ARGUMENT_COMMAND_MALFORMED, ERR_COMMAND_FILE_NOT_FOUND


class Kernel:
    version = WEX_VERSION
    paths: dict[str, Optional[str]] = {
        "root": None
    }

    def __init__(self):
        self.paths['root'] = os.getcwd() + '/'
        self.paths['addons'] = self.paths['root'] + 'addons/'

        # Load the messages from the JSON file
        with open(os.getcwd() + '/locale/messages.json') as f:
            self.messages = json.load(f)

    def trans(self, key: str) -> str:
        return self.messages[key]

    def error(self, code: str) -> None:
        raise click.BadParameter(
            f"[{code}] {self.trans(code)}"
        )

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

        return self.paths['addons'] + '/'.join(parts) + ".py"

    def path_to_module(self, path: str) -> str:
        relative_path = os.path.relpath(path, self.paths['root'])
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
        function_name: str = f"{match.group(1)}_{match.group(2)}_{match.group(3)}"
        module_name: str = self.path_to_module(command_path)
        module: 'ModuleType' = importlib.import_module(module_name)
        function = getattr(module, function_name)

        ctx = function.make_context(command, command_args or ())
        ctx.obj = self
        function.invoke(ctx)
