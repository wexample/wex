import os
from typing import Optional

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.helper.command import execute_command_sync


class NonInteractiveShellCommandResponse(AbstractResponse):
    def __init__(self, kernel, shell_command: list, ignore_error: bool = False):
        super().__init__(kernel)

        self.success: bool | None = None
        self.shell_command: list = shell_command
        self.ignore_error: bool = ignore_error

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: Optional[dict] = None,
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
    ):
        return os.linesep.join(self.output_bag[0])
