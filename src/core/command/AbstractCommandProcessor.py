from __future__ import annotations

import importlib.util
import os
import re
from abc import abstractmethod

from typing import Optional

from src.helper.args import convert_dict_to_args, convert_args_to_dict
from src.const.error import ERR_COMMAND_FILE_NOT_FOUND


class AbstractCommandProcessor:
    command: str
    command_args: []
    kernel: 'Kernel'
    match: Optional[re.Match] = None

    def __init__(self, kernel: 'Kernel', command: str = None, command_args: [] = []):
        self.kernel = kernel
        self.command = command
        self.command_args = command_args

        if command is not None:
            self.match = self.parse(command)

    def exec(self) -> str | None:
        # Get valid path.
        command_path: str = self.get_path()

        if not os.path.isfile(command_path):
            self.kernel.error(ERR_COMMAND_FILE_NOT_FOUND, {
                'command': self.command,
                'path': command_path,
            })
            return

        function = self.get_function(self)

        command_args = self.command_args
        if isinstance(self.command_args, dict):
            command_args = convert_dict_to_args(function, command_args)

        middleware_args = {
            'args': convert_args_to_dict(function, command_args),
            'args_list': command_args,
            'command': self.command,
            'command_type': self.get_type(),
            'function': function,
            'match': self.match,
        }

        self.kernel.exec_middlewares('exec', middleware_args)

        result = self.kernel.exec_function(function, command_args)

        self.kernel.exec_middlewares('exec_post', middleware_args)

        return result

    def get_function(self, kernel) -> str:
        command_path = self.get_path()

        # Import module and load function.
        spec = importlib.util.spec_from_file_location(command_path, command_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(
            module,
            self.get_function_name()
        )

    @abstractmethod
    def get_pattern(self) -> str:
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass

    def parse(self, command):
        return re.match(self.get_pattern(), command)

    @abstractmethod
    def get_path(self, subdir: str = None):
        pass

    @abstractmethod
    def get_function_name(self):
        pass

    def build_full_command_from_function(self, function_or_command, args: dict = None) -> str | None:
        if isinstance(function_or_command, str):
            return function_or_command

        return None


    def build_command_from_function(self, function_or_command) -> str | None:
        if isinstance(function_or_command, str):
            return function_or_command

        return None

    def build_command_path(self, base_path, subdir: str | None, command_path):
        if subdir:
            base_path += f"{subdir}/"

        return os.path.join(base_path, 'command', command_path + '.py')
