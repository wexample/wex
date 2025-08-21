import os
from typing import TYPE_CHECKING, Optional, cast

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.const.types import (
    OptionalCoreCommandArgsDict,
    ResponsePrintType,
    ShellCommandsDeepList,
    ShellCommandsList,
    StringsList,
)
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.helper.command import execute_command_tree_sync

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


class NonInteractiveShellCommandResponse(AbstractResponse):
    def __init__(
        self,
        kernel: "Kernel",
        shell_command: ShellCommandsDeepList | ShellCommandsList,
        ignore_error: bool = False,
        as_sudo_user: bool = True,
        workdir: Optional[str] = None,
    ) -> None:
        super().__init__(kernel)

        self.shell_command = cast(ShellCommandsDeepList, shell_command.copy())
        self.as_sudo_user = as_sudo_user
        self.ignore_error: bool = ignore_error
        self.workdir = workdir
        self.success: Optional[bool] = None

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        success, content = execute_command_tree_sync(
            kernel=self.kernel,
            command_tree=self.shell_command,
            working_directory=self.workdir,
            ignore_error=self.ignore_error,
            as_sudo_user=self.as_sudo_user,
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
        assert isinstance(output_string, list)

        return os.linesep.join(cast(StringsList, output_string))
