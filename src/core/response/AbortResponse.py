from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse

if TYPE_CHECKING:
    from src.const.types import OptionalCoreCommandArgsDict


class AbortResponse(AbstractResponse, ABC):
    def __init__(self, kernel, reason: str):
        super().__init__(kernel)

        self.reason = reason

    def render(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
            args: OptionalCoreCommandArgsDict = None):
        return None

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
            args: OptionalCoreCommandArgsDict = None) -> AbstractResponse:
        # Nothing to do
        return self
