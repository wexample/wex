import os
from typing import TYPE_CHECKING, Match, Optional

from src.const.globals import COMMAND_EXTENSION_PYTHON, COMMAND_EXTENSION_YAML
from src.core.command.ScriptCommand import ScriptCommand
from src.helper.args import args_convert_dict_to_args

if TYPE_CHECKING:
    from src.const.types import OptionalCoreCommandArgsListOrDict, StringsList
    from src.core.command.resolver import AbstractCommandResolver


class CommandRequest:
    def __init__(
        self,
        resolver,
        command: str,
        args: Optional["OptionalCoreCommandArgsListOrDict"] = None,
    ):
        self.extension: None | str = None
        self.quiet = False
        self.resolver: AbstractCommandResolver = resolver
        self.runner = None
        self.string_command = resolver.resolve_alias(command)
        self.type = resolver.get_type()
        self.storage = {}  # Useful to store data about the current command execution
        self.args = args or []
        self.parent = self.resolver.kernel.current_request
        self.path: None | str = None
        self.script_command: Optional[ScriptCommand] = None
        self.first_arg = self.resolver.kernel
        self.match: Optional[Match] = None
        self.localized: bool = False

        self.resolver.locate_function(self)

        if not self.path:
            # Do not return any error if function is missing,
            # as it is managed outside.
            return

    def get_root_parent(self) -> "CommandRequest":
        if self.parent:
            return self.parent.get_root_parent()
        return self

    def load_extension(self, extension: str) -> bool:
        path = self.resolver.build_path(self, extension)

        if path and os.path.isfile(path):
            runner = None

            if extension == COMMAND_EXTENSION_PYTHON:
                from src.core.command.runner.PythonCommandRunner import (
                    PythonCommandRunner,
                )

                runner = PythonCommandRunner(self.resolver.kernel)
            elif extension == COMMAND_EXTENSION_YAML:
                from src.core.command.runner.YamlCommandRunner import YamlCommandRunner

                runner = YamlCommandRunner(self.resolver.kernel)

            self.path = path
            self.extension = extension

            runner.set_request(self)

            self.script_command = self.runner.build_script_command()

            # Runner can now convert args.
            if isinstance(self.args, dict):
                self.args = args_convert_dict_to_args(self.script_command.function, self.args)

            return True

    def get_args_list(self) -> "StringsList":
        if isinstance(self.args, list):
            return self.args.copy()

        return []
