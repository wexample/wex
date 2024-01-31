from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse

if TYPE_CHECKING:
    from src.const.types import OptionalCoreCommandArgsDict


class HasAttachedResponse(AbstractResponse):
    def __init__(self, kernel: "Kernel", response: Optional[Any] = None) -> None:
        super().__init__(kernel)

        self.response: Any = response

    def render_content_append_response(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> None:
        # Allow to return a response even stopping.
        if self.response:
            response_wrapped = self.get_request().resolver.wrap_response(self.response)
            response_wrapped.render_content(
                request,
                render_mode,
                args,
            )

            self.output_bag = response_wrapped.output_bag.copy()
