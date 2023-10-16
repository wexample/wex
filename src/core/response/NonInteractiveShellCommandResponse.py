from src.helper.command import execute_command
from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class NonInteractiveShellCommandResponse(AbstractResponse):
    def __init__(self, kernel, shell_command: list):
        super().__init__(kernel)

        self.success: bool | None = None
        self.shell_command: list = shell_command

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> AbstractResponse:
        success, content = execute_command(
            self.kernel,
            self.shell_command,
        )

        self.success = success

        if success:
            self.output_bag.append(content)

        return self
