from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, List, Optional

from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from src.core.CommandRequest import CommandRequest, HasRequest
from src.core.KernelChild import KernelChild

if TYPE_CHECKING:
    from src.const.types import OptionalCoreCommandArgsDict, ResponsePrintType
    from src.core.Kernel import Kernel


class AbstractResponse(KernelChild, HasRequest):
    def __init__(self, kernel: "Kernel"):
        KernelChild.__init__(self, kernel)
        HasRequest.__init__(self)

        self.parent = None
        self.output_bag: list = []
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
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> None:
        self.set_request(request)
        self.parent = self.kernel.current_response

        # If response passes from a function to another,
        # it may be already rendered.
        if self.rendered:
            return None

        # When reusing response internally,
        # rendering might be delayed.
        if render_mode == KERNEL_RENDER_MODE_NONE:
            return None

        previous_response = self.parent = self.kernel.current_response
        self.kernel.current_response = self

        self.render_content(
            request,
            render_mode,
            args,
        )

        self.kernel.current_response = previous_response
        self.rendered = True

    @abstractmethod
    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> "AbstractResponse":
        pass

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        if len(self.output_bag):
            serialised = []
            for output in self.output_bag:
                if isinstance(output, AbstractResponse):
                    if output.interactive_data or interactive_data:
                        output_serialized = output.print(
                            render_mode=render_mode,
                            interactive_data=interactive_data,
                        )
                        if output_serialized is not None:
                            serialised.append(output_serialized)
                elif output is not None:
                    serialised.append(output)

            if not len(serialised):
                return None

            return serialised

        return None

    def first(self) -> Any:
        """
        Return the first valid response.
        Useful to retrieve result of a function without to serialize it.
        """
        response = self
        while isinstance(response, AbstractResponse):
            if len(response.output_bag):
                response = response.output_bag[0]
            else:
                return response

        return response

    def storable_data(self) -> bool:
        return True

    def store_data(self):
        if self.storable_data() and self.print(
            render_mode=KERNEL_RENDER_MODE_TERMINAL, interactive_data=False
        ):
            return self.first()
        return None

    def render_content_multiple(
        self,
        collection,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: Optional[dict] = None,
    ):
        for response in collection:
            if isinstance(response, AbstractResponse):
                self.output_bag.append(
                    response.render_content(
                        request,
                        render_mode,
                        args,
                    )
                )

    def render_mode_json_wrap_data(self, value):
        return {"value": value}

    def print_wrapped(self, render_mode: str = KERNEL_RENDER_MODE_TERMINAL):
        if render_mode == KERNEL_RENDER_MODE_NONE:
            return None

        value = self.print(render_mode)

        if render_mode == KERNEL_RENDER_MODE_JSON:
            import json

            return json.dumps(self.render_mode_json_wrap_data(value))

        return value


ResponseCollection = List[AbstractResponse]
