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

from typing import TYPE_CHECKING, Any
from pydantic import BaseModel, PrivateAttr

# Stay lazy as most as possible
if TYPE_CHECKING:
    # Only for static typing
    from somewhere import SomeType


class MyClass(BaseModel):
    _internal_var: "SomeType" = PrivateAttr()

    # model_post_init runs AFTER Pydantic has validated/coerced model fields.
    # Use it to initialize PrivateAttr that may rely on validated state.
    # If you depend on other mixins' __init__ ordering, prefer a custom __init__ or finalize().
    def model_post_init(self, __context: Any) -> None:
        # Lazy import at runtime to avoid circular imports
        from somewhere import SomeType
        self._internal_var = SomeType(property="Yes")

    @property
    def public_var(self) -> "SomeType":
        # Getter is non-optional and always returns a conformant type
        return self._internal_var

    @public_var.setter
    def public_var(self, value: "SomeType") -> None:
        # Lazy import for runtime type checking
        from somewhere import SomeType
        # Check value at setting, avoid checking it elsewhere
        if not isinstance(value, SomeType):
            raise TypeError(f"public_var must be SomeType, got {type(value)!r}")
        self._internal_var = value
```

### Variant: when mixins must run before initialization

Use a custom `__init__`  and set the private attribute after all mixins are initialized.

```
class MyService(MixinClass, BaseModel):
    name: str
    
    def __init__(self, **kwargs):
        # Pydantic should be initialized first to allow mixins playing with it.
        BaseModel.__init__(self, **kwargs)
        MixinClass.__init__(self)
        
        self._internal_var = SomeType(property=self.name)