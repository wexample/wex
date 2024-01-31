from __future__ import annotations

from src.core.response.AbortResponse import AbortResponse
from typing import TYPE_CHECKING, Any
from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse

if TYPE_CHECKING:
    from src.const.types import OptionalCoreCommandArgsDict


class QueuedCollectionStopResponse(AbortResponse):
    def __init__(self, kernel: "Kernel", reason: str, response: Any = None) -> None:
        super().__init__(kernel, reason)

        self.reason = reason
        self.response: Any = response

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        # Allow to return a response even stopping.
        if self.response:
            response_wrapped = self.get_request().resolver.wrap_response(self.response)
            response_wrapped.render_content(
                request,
                render_mode,
                args,
            )

            self.output_bag = response_wrapped.output_bag.copy()

        return super().render_content(
            request,
            render_mode,
            args,
        )
