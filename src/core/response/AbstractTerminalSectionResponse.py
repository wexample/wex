from __future__ import annotations

from abc import ABC

from src.core.response.AbstractResponse import AbstractResponse


class AbstractTerminalSectionResponse(AbstractResponse, ABC):
    def __init__(self, kernel, title: None = None):
        super().__init__(kernel)
        self.title = title

    def set_title(self, title):
        self.title = title

    def render_cli_title(self, line_width: int) -> str:
        # Add title if exists, aligned to the left and fill with underscores
        if self.title:
            # Calculate how much padding is needed on each side of the title
            title_length = len(self.title)
            # remove 2 for title margins
            padding_each_side = (line_width - title_length - 2) // 2

            # Check if we need an extra '=' at the end (for odd width)
            extra_equal = "=" if (line_width - title_length) % 2 == 1 else ""

            # Construct the title line
            return f"{'=' * padding_each_side} {self.title} {'=' * padding_each_side}{extra_equal}\n"

        return ''
