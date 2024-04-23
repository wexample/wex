from typing import Optional

from pydantic import BaseModel

from addons.ai.src.assistant.model.reliable_value import ReliableValue


class Person(BaseModel):
    first_name: ReliableValue
    last_name: ReliableValue
    age: ReliableValue
    email: Optional[ReliableValue] = None
