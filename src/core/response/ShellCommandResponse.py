from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class ShellCommandResponse(AbstractResponse):
    def __init__(self, kernel, shell_command: list):
        super().__init__(kernel)

        self.shell_command: list = shell_command

    def render(self, kernel, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        return 'SHELL'
