from __future__ import annotations

import os
import shutil
from abc import ABC
from typing import TYPE_CHECKING, Optional, cast

from src.const.types import JsonContent, ResponsePrintType
from src.core.response.AbstractResponse import AbstractResponse

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


class AbstractTerminalSectionResponse(AbstractResponse, ABC):
    def __init__(
        self,
        kernel: "Kernel",
        title: str | None = None,
        default_render_mode: Optional[str] = None,
    ) -> None:
        super().__init__(kernel, default_render_mode)
        self.title: str | None = title

    def render_cli_title(self, line_width: Optional[int] = None) -> str:
        terminal_width, _ = shutil.get_terminal_size()
        line_width = (
            terminal_width
            if (not line_width or line_width > terminal_width)
            else line_width
        )

        # Add title if exists, aligned to the left and fill with underscores
        if self.title:
            # Calculate how much padding is needed on each side of the title
            title_length = len(self.title)
            # remove 2 for title margins
            padding_each_side = (line_width - title_length - 2) // 2

            # Check if we need an extra '=' at the end (for odd width)
            extra_equal = "=" if (line_width - title_length) % 2 == 1 else ""

            # Construct the title line
            return f"{'=' * padding_each_side} {self.title} {'=' * padding_each_side}{extra_equal}{os.linesep}"

        return ""

    def render_mode_json_wrap_data(self, value: ResponsePrintType) -> JsonContent:
        # Do not add extra json wrapping
        return cast(JsonContent, value)
