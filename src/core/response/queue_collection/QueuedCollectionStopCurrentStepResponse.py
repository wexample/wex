from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.const.types import OptionalCoreCommandArgsDict
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractEmptyResponse import AbstractEmptyResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.queue_collection.HasAttachedResponse import HasAttachedResponse

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class QueuedCollectionStopCurrentStepResponse(
    AbstractEmptyResponse, HasAttachedResponse
):
    def __init__(
        self, kernel: "Kernel", reason: str, response: Optional[Any] = None
    ) -> None:
        AbstractEmptyResponse.__init__(self, kernel, reason)
        HasAttachedResponse.__init__(self, kernel, response)

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        self.render_content_append_response(
            request,
            render_mode,
            args,
        )

        return super().render_content(
            request,
            render_mode,
            args,
        )
