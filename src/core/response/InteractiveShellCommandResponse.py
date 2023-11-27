import os
from typing import Optional

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.helper.command import command_to_string, execute_command_sync
from src.helper.process import process_post_exec


class InteractiveShellCommandResponse(AbstractResponse):
    def __init__(self, kernel, shell_command: list | str, ignore_error: bool = False):
        super().__init__(kernel)

        if isinstance(shell_command, list):
            shell_command = list(shell_command)

        self.shell_command: list | str = shell_command
        self.interactive_data = True
        self.ignore_error = ignore_error

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: Optional[dict] = None,
    ) -> AbstractResponse:
        if self.ignore_error:
            self.shell_command += ["||", "true"]

        if self.kernel.fast_mode:
            # When using fast mode, we need to preserve consistency between shell executions.
            # Ex : ['echo', '"OK"'] should return OK without quotes.
            # As we don't use shlex to wrap arguments,
            # we need to enable shell=True here.

            success, content = execute_command_sync(
                self.kernel, command_to_string(self.shell_command), shell=True
            )

            self.success = success

            # Output data as it was printed in a shell.
            self.output_bag.append(os.linesep.join(content))

        # Do not add to render bag, but append only once.
        elif not self.rendered:
            process_post_exec(self.kernel, self.shell_command)

        return self

    def storable_data(self) -> bool:
        return False

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> str | None:
        return self.output_bag[0] if len(self.output_bag) else None
