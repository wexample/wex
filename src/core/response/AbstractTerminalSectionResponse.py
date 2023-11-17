from __future__ import annotations

import shutil
from abc import ABC
from src.core.response.AbstractResponse import AbstractResponse


class AbstractTerminalSectionResponse(AbstractResponse, ABC):
    def __init__(self, kernel, title: str | None = None):
        super().__init__(kernel)
        self.title = title

    def set_title(self, title):
        self.title = title

    def render_cli_title(self, title: str, line_width: int) -> str:
        terminal_width, _ = shutil.get_terminal_size()
        line_width = terminal_width if line_width > terminal_width else line_width

        # Add title if exists, aligned to the left and fill with underscores
        if title:
            # Calculate how much padding is needed on each side of the title
            title_length = len(title)
            # remove 2 for title margins
            padding_each_side = (line_width - title_length - 2) // 2

            # Check if we need an extra '=' at the end (for odd width)
            extra_equal = "=" if (line_width - title_length) % 2 == 1 else ""

            # Construct the title line
            return f"{'=' * padding_each_side} {title} {'=' * padding_each_side}{extra_equal}\n"

        return ''

    def render_mode_json_wrap_data(self, value):
        # Do not add extra json wrapping
        return value
