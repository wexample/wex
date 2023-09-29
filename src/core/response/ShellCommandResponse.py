import subprocess

from src.core.CommandRequest import CommandRequest
from src.helper.process import process_post_exec
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class ShellCommandResponse(AbstractResponse):
    def __init__(self, kernel, shell_command: list):
        super().__init__(kernel)

        self.shell_command: list = shell_command

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> AbstractResponse:
        if self.kernel.allow_post_exec:
            process_post_exec(
                self.kernel,
                self.shell_command
            )
        else:
            subprocess.run(self.shell_command, capture_output=True).stdout.decode('utf-8')

        return self
