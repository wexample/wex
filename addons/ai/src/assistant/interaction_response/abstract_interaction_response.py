from __future__ import annotations

from typing import Optional


class AbstractInteractionResponse(object):
    def render(self) -> Optional[str]:
        return None
