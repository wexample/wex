from abc import abstractmethod

from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_CLI


class AbstractResponse:
    def __init__(self, kernel):
        # Prevent circular imports
        from src.core.Kernel import Kernel

        self.request = kernel.current_request
        self.kernel: Kernel = kernel
        self.parent = None
        self.output_bag: list = []

    def get_root_parent(self):
        if self.parent:
            return self.parent.get_root_parent()
        return self

    @abstractmethod
    def render(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None):
        pass

    def print(self) -> str | None:
        if len(self.output_bag):
            serialised = []
            for output in self.output_bag:
                if isinstance(output, AbstractResponse):
                    output_serialized = output.print()
                    if output_serialized is not None:
                        serialised.append(output_serialized)
                else:
                    serialised.append(str(output))

            if not len(serialised):
                return None

            return '\n'.join(serialised)

        return None
