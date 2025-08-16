# Python Guidelines

You are reading this file because you want information about project specific Pydantic coding style.

## General requirements
- Always use Pydantic v2

## Rules
- Follow latest Pydantic coding style
- Never add this, except if explicitly asked for, let it in place if already set up:
  - `model_config = ConfigDict(arbitrary_types_allowed=True)`
  - `class ``Config: ... arbitrary_types_allowed = True`

## Internal property

How to define a variable from inside a class, publicly accessible, and type checked 

```
from __future__ import annotations

from typing import TYPE_CHECKING
from pydantic import BaseModel, PrivateAttr

# Stay lazy as most as possible
if TYPE_CHECKING:
    from somewhere import SomeType


class MyClass(BaseModel):
    _internal_var: "SomeType" = PrivateAttr()

    def __init__(**kwargs):
        BaseModel.__init__(self, **kwargs)
        from somewhere import SomeType
        self._internal_var = SomeType(property="Yes")

    @property
    def public_var(self) -> "SomeType":
        return self._internal_var

    @public_var.setter
    def public_var(self, value: "SomeType") -> None:
        # Stay lazy as most as possible
        from somewhere import SomeType
        # Check value at setting, avoid checking it 
        if not isinstance(value, SomeType):
            raise TypeError(f"internal_var must be SomeType, got {type(value)!r}")
        self._internal_var = value