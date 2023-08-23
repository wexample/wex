from __future__ import annotations

import importlib.util
import os
import re
from abc import abstractmethod

from typing import Optional

from src.helper.args import convert_dict_to_args, convert_args_to_dict
from src.const.error import ERR_COMMAND_FILE_NOT_FOUND
from src.helper.file import set_owner_recursive
from src.helper.string import trim_leading
from src.helper.system import get_user_or_sudo_user


class AbstractCommandProcessor:
    command: str
    command_args: []
    kernel: 'Kernel'
    match: Optional[re.Match] = None

    def __init__(self, kernel: 'Kernel', command: str = None, command_args: [] = []):
        self.kernel = kernel

        self.set_command(
            command,
            command_args
        )

    def exec(self) -> str | None:
        # Get valid path.
        command_path: str = self.get_path()

        if not os.path.isfile(command_path):
            self.kernel.error(ERR_COMMAND_FILE_NOT_FOUND, {
                'command': self.command,
                'path': command_path,
            })
            return

        function = self.get_function()

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

    def get_function(self) -> str:
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

    @staticmethod
    def get_commands_registry(kernel) -> dict:
        return {}

    @abstractmethod
    def get_type(self) -> str:
        pass

    def get_base_path(self) -> str | None:
        return None

    def get_base_command_path(self) -> str | None:
        base_path = self.get_base_path()

        if not base_path:
            return None

        return os.path.join(base_path, 'command') + '/'

    def set_command_file_permission(self, command_path: str):
        base_path = self.get_base_path()

        if base_path:
            set_owner_recursive(
                base_path,
                trim_leading(command_path, base_path),
                get_user_or_sudo_user(),
            )

    def set_command(self, command: str | None, args: [] = []):
        self.command = command
        self.command_args = args
        self.match = re.match(self.get_pattern(), command) if command else None

        return self.match

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

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        return None

    def suggest_arguments(self, command: str, search_params: []):
        self.set_command(
            command
        )

        # Command is not recognised
        if not self.match:
            return

        # File does not exist
        if not os.path.isfile(self.get_path()):
            return

        search_params = [val for val in search_params if val.startswith("-")]

        # Merge all params in a list,
        # but ignore already given args,
        # i.e : if -d is already given, do not suggest "-d" or "--default"
        function = self.get_function()

        params = []
        for param in function.params:
            if any(opt in search_params for opt in param.opts):
                continue

            params += param.opts

        return ' '.join(params)
