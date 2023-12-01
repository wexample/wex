import os
from typing import TYPE_CHECKING

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.const.types import (
    OptionalCoreCommandArgsDict,
    ResponsePrintType,
    ShellCommandsList,
)
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.helper.command import execute_command_sync

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class NonInteractiveShellCommandResponse(AbstractResponse):
    def __init__(
        self,
        kernel: "Kernel",
        shell_command: ShellCommandsList,
        ignore_error: bool = False,
    ) -> None:
        super().__init__(kernel)

        self.success: bool | None = None
        self.shell_command: ShellCommandsList = shell_command
        self.ignore_error: bool = ignore_error

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        success, content = execute_command_sync(
            kernel=self.kernel,
            command=self.shell_command,
            ignore_error=self.ignore_error,
        )

        self.success = success

        if success:
            self.output_bag.append(content)

        return self

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        if not len(self.output_bag):
            return None

        output_string = self.output_bag[0]
        assert isinstance(output_string, str)

        return os.linesep.join(output_string)
