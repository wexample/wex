from __future__ import annotations
from typing import cast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.abc import Loader


def module_load_from_file(file_path: str, module_name: str) -> Loader:
    from importlib.abc import Loader
    from importlib import util
    from importlib.machinery import ModuleSpec

    spec = util.spec_from_file_location(module_name, file_path)
    assert isinstance(spec, ModuleSpec)
    module = util.module_from_spec(spec)
    assert isinstance(spec.loader, Loader)
    spec.loader.exec_module(module)
    return cast(Loader, module)
