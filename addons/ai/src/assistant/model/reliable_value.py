from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class ReliableValue(BaseModel):
    reliability: Literal["reliable", "unreliable", "dubious"]
    value: str | int | None
