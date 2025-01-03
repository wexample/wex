from typing import Literal, Union

from pydantic import BaseModel


class ReliableValue(BaseModel):
    value: Union[str, int, None]
    reliability: Literal["reliable", "unreliable", "dubious"]
