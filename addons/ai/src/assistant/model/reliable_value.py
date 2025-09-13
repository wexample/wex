from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class ReliableValue(BaseModel):
    value: str | int | None
    reliability: Literal["reliable", "unreliable", "dubious"]
