import os
from typing import TYPE_CHECKING, Optional, cast

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.const.types import (OptionalCoreCommandArgsDict, ResponsePrintType,
                             ShellCommandsDeepList, ShellCommandsList)
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.helper.command import execute_command_tree_sync

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


class InteractiveShellCommandResponse(AbstractResponse):
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
        self.interactive_data = True
        self.as_sudo_user = as_sudo_user
        self.ignore_error = ignore_error
        self.workdir = workdir
        self.success: Optional[bool] = None

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        success, content = execute_command_tree_sync(
            self.kernel,
            command_tree=self.shell_command,
            working_directory=self.workdir,
            ignore_error=self.ignore_error,
            as_sudo_user=self.as_sudo_user,
            interactive=True,
        )

        self.success = success

        # Output data as it was printed in a shell.
        self.output_bag.append(os.linesep.join(content))

        return self

    def storable_data(self) -> bool:
        return False

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            return self.get_first_output_printable_value()
        return self.output_bag
