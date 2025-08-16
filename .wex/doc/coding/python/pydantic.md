# Python Guidelines

You are reading this file because you want information about project specific Pydantic coding style.

## Rules
- Follow latest Pydantic coding style
- Never add this, except if explicitly asked for, let it in place if already set up:
  - `model_config = ConfigDict(arbitrary_types_allowed=True)`
  - `class Config: ... arbitrary_types_allowed = True`

### Internal property

How to define a variable from inside a class, publicly accessible, and type checked 