import subprocess

from src.helper.command import command_to_string
from src.core.CommandRequest import CommandRequest
from src.helper.process import process_post_exec
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class InteractiveShellCommandResponse(AbstractResponse):
    def __init__(self, kernel, shell_command: list):
        super().__init__(kernel)

        self.shell_command: list = shell_command
        self.interactive_data = True

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> AbstractResponse:
        if self.kernel.fast_mode:
            # When using fast mode, we need to preserve consistency between shell executions.
            # Ex : ['echo', '"OK"'] should return OK without quotes.
            # As we don't use shlex to wrap arguments,
            # we need to enable sell=True here.
            self.output_bag.append(
                subprocess
                .run(command_to_string(self.shell_command),
                     capture_output=True,
                     shell=True)
                .stdout.
                decode('utf-8').strip())
        else:
            process_post_exec(
                self.kernel,
                self.shell_command
            )

        return self
