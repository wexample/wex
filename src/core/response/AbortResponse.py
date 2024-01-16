from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL, VERBOSITY_LEVEL_MAXIMUM
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractEmptyResponse import AbstractEmptyResponse
from src.core.response.AbstractResponse import AbstractResponse

if TYPE_CHECKING:
    from src.const.typing import OptionalCoreCommandArgsDict


class AbortResponse(AbstractEmptyResponse, ABC):
    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        # Nothing to do
        self.kernel.io.log(
            f"Aborting : {self.reason}", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )

        return super().render_content(
            request,
            render_mode,
            args,
        )
