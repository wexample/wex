from typing import TYPE_CHECKING

from langchain.tools import BaseTool

from src.const.types import Kwargs, Args

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class CommandTool(BaseTool):
    kernel: "Kernel"
    name = "Undefined commands"
    description = "A command to execute"

    def __init__(
        self, kernel: "Kernel", command_name: str, command_description: str, **kwargs: Kwargs
    ):
        super().__init__(**kwargs)
        self.kernel = kernel

        self.name = command_name
        self.description = command_description

    def _run(self, *args: Args) -> str:
        return self.kernel.run_command(self.name, {}).print_wrapped_str()
