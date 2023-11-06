from __future__ import annotations

from abc import ABC

from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class QueuedCollectionStopResponse(AbstractResponse, ABC):
    def __init__(self, kernel, reason: str | None = None):
        super().__init__(kernel)
        self.reason: str | None = reason

    def render(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None):
        return None
