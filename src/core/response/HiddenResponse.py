from __future__ import annotations

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.const.types import ResponsePrintType
from src.core.response.DefaultResponse import DefaultResponse


class HiddenResponse(DefaultResponse):
    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        if interactive_data:
            return None

        return super().print(interactive_data=interactive_data, render_mode=render_mode)
