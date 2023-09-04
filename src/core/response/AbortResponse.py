from __future__ import annotations

from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class AbortResponse(AbstractResponse):
    def __init__(self, kernel):
        super().__init__(kernel)

    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI, args: dict = None) -> str | int | bool | None:
        return None
