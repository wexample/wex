from __future__ import annotations

from src.core.response.DefaultResponse import DefaultResponse


class ResponseCollectionHiddenResponse(DefaultResponse):
    def print(self, interactive_data: bool = True) -> str | None:
        if interactive_data:
            return None

        return super().print(
            interactive_data=interactive_data,
        )
