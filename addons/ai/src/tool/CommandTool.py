from langchain.tools import BaseTool

from src.const.types import Args, Kwargs
from src.core.Kernel import Kernel


class CommandTool(BaseTool):
    kernel: Kernel
    name: str
    description: str

    def __init__(self, **kwargs: Kwargs):
        super().__init__(**kwargs)

    def _run(self, *args: Args, **kwargs: Kwargs) -> str:
        return self.kernel.run_command(self.name, {}).print_wrapped_str()
