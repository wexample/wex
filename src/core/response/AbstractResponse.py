from __future__ import annotations
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
        self.request = None
        self.parent = None
        self.rendered = False
        # Some data can ba part of the output
        # but cannot be sent to the next functions call,
        # we call it "interactive".
        self.interactive_data = False

    def get_root_parent(self):
        if self.parent:
            return self.parent.get_root_parent()
        return self

    def render(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> 'AbstractResponse':
        self.request = request
        self.parent = self.kernel.current_response

        previous_response = self.parent = self.kernel.current_response
        self.kernel.current_response = self

        # Save root response once.
        self.kernel.root_response = self.kernel.root_response or self

        output = self.render_content(
            request,
            render_mode,
            args,
        )

        self.kernel.current_response = previous_response
        self.rendered = True

        return output

    @abstractmethod
    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> 'AbstractResponse':
        pass

    def print(self, interactive_data: bool = True) -> str | None:
        if len(self.output_bag):
            serialised = []
            for output in self.output_bag:
                if isinstance(output, AbstractResponse):
                    if not output.interactive_data or interactive_data:
                        output_serialized = output.print(interactive_data)
                        if output_serialized is not None:
                            serialised.append(output_serialized)
                else:
                    serialised.append(str(output))

            if not len(serialised):
                return None

            return '\n'.join(serialised)

        return None
