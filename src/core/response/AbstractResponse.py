from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, List, Optional, cast

from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from src.const.types import (
    AnyList,
    Args,
    JsonContent,
    OptionalCoreCommandArgsDict,
    ResponsePrintType,
)
from src.core.BaseClass import BaseClass
from src.core.CommandRequest import CommandRequest, HasRequest
from src.core.KernelChild import KernelChild

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class AbstractResponse(KernelChild, HasRequest):
    def __init__(
        self, kernel: "Kernel", default_render_mode: Optional[str] = None
    ) -> None:
        KernelChild.__init__(self, kernel)
        HasRequest.__init__(self)

        self._default_render_mode = default_render_mode
        self.parent: Optional["AbstractResponse"] = None
        self.output_bag: List[ResponsePrintType | AbstractResponse] = []
        self.parent = None
        self.rendered = False
        # This may be used only by queued responses,
        # but we need to check the "real end" of command
        # in more global context.
        self.has_next_step: bool = False
        # Some data can ba part of the output
        # but cannot be sent to the next functions call,
        # we call it "interactive".
        self.interactive_data = False

    def get_root_parent(self) -> "AbstractResponse":
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

    def get_one(self, position: int) -> Any:
        """
        Return recursively the Xth item of the output bag.
        Mainly used to retrieve the bare first or last one.
        """
        response: Any = self
        while isinstance(response, AbstractResponse):
            if len(response.output_bag):
                response = response.output_bag[position]
            else:
                return response

        return response

    def first(self) -> Any:
        return self.get_one(0)

    def last(self) -> Any:
        return self.get_one(-1)

    def storable_data(self) -> bool:
        return True

    def store_data(self) -> Any:
        if self.storable_data() and self.print(
            render_mode=KERNEL_RENDER_MODE_TERMINAL, interactive_data=False
        ):
            return self.first()
        return None

    def render_content_multiple(
        self,
        collection: AnyList,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> None:
        for response in collection:
            if isinstance(response, AbstractResponse):
                self.output_bag.append(
                    response.render_content(
                        request,
                        render_mode,
                        args,
                    )
                )

    def render_mode_json_wrap_data(self, value: ResponsePrintType) -> JsonContent:
        return {"value": value}

    def print_wrapped(
        self, render_mode: str = KERNEL_RENDER_MODE_TERMINAL
    ) -> Optional[str]:
        if render_mode == KERNEL_RENDER_MODE_NONE:
            return None

        value = self.print(render_mode)

        if render_mode == KERNEL_RENDER_MODE_JSON:
            import json

            return json.dumps(self.render_mode_json_wrap_data(value))

        return str(value) if value is not None else None

    def print_wrapped_str(self, render_mode: str = KERNEL_RENDER_MODE_TERMINAL) -> str:
        return str(self.print_wrapped(render_mode))

    def get_first_output_printable_value(self) -> ResponsePrintType:
        if not len(self.output_bag):
            return None

        data = self.output_bag[0]
        assert isinstance(data, str | int | float | bool | None | list | dict)

        # can be empty in "none" render mode.
        return cast(ResponsePrintType, data)

    def get(self, *args: Args) -> AbstractResponse:
        current_element: AbstractResponse = self
        for index in args:
            try:
                response = current_element.output_bag[index]
                assert isinstance(response, AbstractResponse)
                current_element = response
            except (IndexError, AttributeError):
                return self.kernel.io.error("Trying to access a out of range response")

        assert isinstance(current_element, AbstractResponse)

        return current_element


class HasResponse(BaseClass):
    def __init__(self) -> None:
        self._response: None | AbstractResponse = None

    def set_response(self, response: AbstractResponse) -> None:
        self._response = response

    def get_response(self) -> AbstractResponse:
        self._validate__should_not_be_none(self._response)
        assert self._response is not None

        return self._response


ResponseCollection = List[AbstractResponse]
