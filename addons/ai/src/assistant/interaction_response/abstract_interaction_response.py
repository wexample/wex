from __future__ import annotations

from typing import Optional


class AbstractInteractionResponse:
    def render(self) -> str | None:
        return None
