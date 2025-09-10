## Class and Field Conventions

We use [`attrs`](https://www.attrs.org) with a thin wrapper to define all data classes.
The goals are: consistent field declarations, automatic `__init__`, and clear distinction between public and private fields.

### Rules

* Always decorate classes with `@base_class`
* Use `public_field` for visible fields

    * `default=...` for scalars
    * `factory=...` for mutable containers (`list`, `dict`, `set`)
* Use `private_field` for internal fields (names starting with `_`)

    * Always excluded from `__init__`
* Add an English `description` to **every field**
* If extra initialization logic is needed, use `__attrs_post_init__` instead of overriding `__init__`

### Example

```python
@base_class
class ExampleClass(BaseClass):
    name: str = public_field(
        description="Name of the entity"
    )
    tags: list[str] = public_field(
        factory=list,
        description="List of associated tags"
    )
    active: bool = public_field(
        default=True,
        description="Indicates whether the entity is active"
    )
    _cache: dict[str, Any] = private_field(
        default=None,
        description="Internal cache for runtime data"
    )

    def __attrs_post_init__(self) -> None:
        if not self.name:
            raise ValueError("name is required")
```
