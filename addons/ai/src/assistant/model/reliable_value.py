from typing import Union, Literal

from pydantic import BaseModel


class ReliableValue(BaseModel):
    value: Union[str, int, None]
    reliability: Literal["reliable", "unreliable", "dubious"]
