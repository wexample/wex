# Python Spacing Rules

## File Level

- **0 blank lines** before module docstring
- **1 blank line** after module docstring (if present)
- **1 blank line** after imports block
- **1 blank line** after type checking imports block
- **0 blank lines** between imports within same group
- **1 blank line** between import groups (stdlib, third-party, local)

## Classes

- **2 blank lines** before class definition
- **1 blank line** after class docstring (if present)
- **0 blank lines** between consecutive class properties (comments allowed)
- **1 blank line** between class methods
- **0 blank lines** after method signature (stick to docstring/first statement)
- **0 blank lines** before final return/last control structure

## Functions

- **2 blank lines** before module-level function definition
- **1 blank line** after function docstring (if present)
- **0 blank lines** after function signature (stick to docstring/first statement)
- **0 blank lines** before final return/last control structure

## Control Structures

- **0 blank lines** after `if`, `elif`, `else`, `for`, `while`, `try`, `except`, `finally`
- **0 blank lines** before `elif`, `else` (unless comment between)
- **1 blank line** after complete control block (except at function/method end)
- **0 blank lines** around nested control structures
- **1 blank line** between distinct logical blocks at same indentation level

## Comments

- Block comments follow same spacing rules as code they precede
- Inline comments allowed without affecting spacing rules