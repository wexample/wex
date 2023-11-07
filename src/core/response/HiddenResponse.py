from __future__ import annotations

from src.core.response.DefaultResponse import DefaultResponse


class HiddenResponse(DefaultResponse):
    def print(self, render_mode: str, interactive_data: bool = True) -> str | None:
        if interactive_data:
            return None

        return super().print(
            interactive_data=interactive_data,
        )
