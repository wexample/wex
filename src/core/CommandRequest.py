import os
from typing import TYPE_CHECKING, Any, Match, Optional

from src.const.globals import COMMAND_EXTENSION_PYTHON, COMMAND_EXTENSION_YAML
from src.const.types import (
    CoreCommandArgsList,
    CoreCommandArgsListOrDict,
    OptionalCoreCommandArgsListOrDict,
    StringKeysDict, StringsMatch,
)
from src.core.BaseClass import BaseClass
from src.core.command.ScriptCommand import ScriptCommand
from src.helper.args import args_convert_dict_to_args

if TYPE_CHECKING:
    from src.core.command.resolver.AbstractCommandResolver import (
        AbstractCommandResolver,
    )
    from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner


class CommandRequest(BaseClass):
    def __init__(
        self,
        resolver: "AbstractCommandResolver",
        command: str,
        args: Optional["OptionalCoreCommandArgsListOrDict"] = None,
    ) -> None:
        self._path: None | str = None
        self._script_command: Optional[ScriptCommand] = None
        self._string_command: str = resolver.resolve_alias(command)
        self._args_source: "CoreCommandArgsListOrDict" = args or []
        self._args_list: Optional[CoreCommandArgsList] = []
        self._runner: Optional["AbstractCommandRunner"] = None

        self.extension: None | str = None
        self.quiet: bool = False
        self.resolver: "AbstractCommandResolver" = resolver
        self.type: str = resolver.get_type()
        self.storage: StringKeysDict = (
            {}
        )  # Useful to store data about the current command execution

        self.parent = self.resolver.kernel.current_request
        self.first_arg: Any = self.resolver.kernel
        self.match: Optional[StringsMatch] = None
        self.localized: bool = False

        self.resolver.locate_function(self)

        if not self._path:
            # Do not return any error if function is missing,
            # as it is managed outside.
            return

    def set_path(self, path: str) -> None:
        self._path = path

    def get_path(self) -> str:
        self._validate__should_not_be_none(self._path)
        assert self._path is not None

        return self._path

    def set_args_list(self, args_list: CoreCommandArgsList) -> None:
        self._args_list = args_list

    def get_args_list(self) -> CoreCommandArgsList:
        self._validate__should_not_be_none(self._args_list)
        assert self._args_list is not None

        return self._args_list

    def set_script_command(self, script_command: ScriptCommand) -> None:
        self._script_command = script_command

    def get_script_command(self) -> ScriptCommand:
        self._validate__should_not_be_none(self._script_command)
        assert self._script_command is not None

        return self._script_command

    def set_string_command(self, string_command: str) -> None:
        self._string_command = string_command

    def get_string_command(self) -> str:
        self._validate__should_not_be_none(self._string_command)
        assert self._string_command is not None

        return self._string_command

    def set_runner(self, runner: "AbstractCommandRunner") -> None:
        self._runner = runner

    def get_runner(self) -> "AbstractCommandRunner":
        self._validate__should_not_be_none(self._runner)
        assert self._runner is not None

        return self._runner

    def get_match(self) -> StringsMatch:
        self._validate__should_not_be_none(self.match)
        assert self.match is not None

        return self.match

    def get_root_parent(self) -> "CommandRequest":
        if self.parent:
            return self.parent.get_root_parent()
        return self

    def load_extension(self, extension: str) -> bool:
        path = self.resolver.build_path(self, extension)

        if path and os.path.isfile(path):
            runner: Optional["AbstractCommandRunner"] = None

            if extension == COMMAND_EXTENSION_PYTHON:
                from src.core.command.runner.PythonCommandRunner import (
                    PythonCommandRunner,
                )

                runner = PythonCommandRunner(self.resolver.kernel)
            elif extension == COMMAND_EXTENSION_YAML:
                from src.core.command.runner.YamlCommandRunner import YamlCommandRunner

                runner = YamlCommandRunner(self.resolver.kernel)

            if runner:
                self.set_path(path)
                self.extension = extension

                runner.set_request(self)

                script_command = self.get_runner().build_script_command()

                if script_command:
                    self.set_script_command(script_command)

                    # Runner can now convert args.
                    if isinstance(self._args_source, dict):
                        self.set_args_list(
                            args_convert_dict_to_args(
                                script_command.click_command, self._args_source
                            )
                        )
                    else:
                        self.set_args_list(self._args_source.copy())

                    return True

        return False


class HasRequest(BaseClass):
    def __init__(self) -> None:
        self._request: None | CommandRequest = None

    def set_request(self, request: CommandRequest) -> None:
        self._request = request

    def get_request(self) -> CommandRequest:
        self._validate__should_not_be_none(self._request)
        assert self._request is not None

        return self._request
