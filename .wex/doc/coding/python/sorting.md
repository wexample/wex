# Python Code Reordering Guidelines

This document describes the ordering rules applied by the **code reordering operation**.
The goal is to keep Python files and class definitions organized, predictable, and easy to navigate, without breaking functionality.

---

## File-Level Ordering

- **Module docstring** (single `"""` allowed at top-level).
- **`from __future__ import …`** (always first if present).
- **Imports** (sorted separately with `isort`).
- **`if TYPE_CHECKING:` block** (typing-only imports).
- **Module metadata** (`__all__`, `__version__`, `__author__`, …).
- **Constants** (`UPPER_CASE`, sorted A–Z).
- **Types & aliases** (`Protocol`, `TypedDict`, `NewType`, `TypeAlias`, `Enum`, …).
- **Module-level functions**

  * Public (A–Z).
  * Private (`_…`) (A–Z).
  * Note: `@overload` groups must remain attached to their implementation.
- **Classes** (A–Z by name).
- **`if __name__ == "__main__":`** (always last).

### Exceptions

* **Enum members** → order is preserved (may be semantically relevant).
* **Dataclass fields** → order is preserved (affects generated `__init__`).

---

## Class-Level Ordering

- **Class header & decorators** (`@dataclass`, `@final`, `metaclass=…`).
- **Class docstring**.
- **Class attributes**

  * Special ones first (`__slots__`, `__match_args__`, pydantic `Config`, …).
  * Then public (A–Z).
  * Then private/protected (A–Z).
- **Special methods (`__dunder__`)**

  * Ordered logically (not alphabetically):

    * Construction: `__new__`, `__init__`.
    * Representation: `__repr__`, `__str__`, …
    * Comparison/hash: `__lt__`, … `__eq__`, `__hash__`.
    * Truthiness: `__bool__`.
    * Attribute access: `__getattribute__`, `__getattr__`, …
    * Container/iteration: `__len__`, `__iter__`, `__getitem__`, …
    * Callable: `__call__`.
    * Context managers: `__enter__`, `__exit__`, `__aenter__`, `__aexit__`.
    * Async protocols: `__await__`, `__aiter__`, …
    * Descriptors/pickling: `__get__`, `__set__`, `__getstate__`, …
  * This fixed order avoids surprising behavior.
- **Class methods (`@classmethod`)**

  * Public (A–Z).
  * Private (A–Z).
- **Static methods (`@staticmethod`)**

  * Public (A–Z).
  * Private (A–Z).
- **Properties**

  * Grouped by property name (getter + setter + deleter kept together).
  * Groups sorted A–Z by property name.
- **Instance methods**

  * Public (A–Z).
  * Private/protected (A–Z).
- **Nested classes / inner types** (A–Z).

---

## Sorting Rules

* **Case-insensitive A–Z**, with `_` ordered *after* letters:
  `a < b < … < z < _a < __a`.
* **Never split logical groups**:

  * `@overload` series + implementation.
  * Properties (`@property`, setter, deleter).
  * Enum members.
  * Dataclass fields.
* **Async variants** (`async def`) follow their sync counterparts if both exist.
* **Docstrings** are allowed for modules, classes, and functions/methods.

---

## Classmethod vs. Staticmethod

* Use **`@classmethod`** for alternate constructors or when class context (`cls`) is required.
* Use **`@staticmethod`** for pure helpers without `self`/`cls`.
* In ordering, **class methods come before static methods** (closer to construction logic).

---

## Summary

This reordering scheme ensures:

* Predictable grouping of structures.
* Alphabetical consistency within safe categories.
* Preservation of functional semantics (no breaking dataclasses, enums, or overloads).

