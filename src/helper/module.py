import importlib
from importlib.abc import Loader
from importlib.machinery import ModuleSpec


def module_load_from_file(file_path: str, module_name: str) -> Loader:
    # Import the test module
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    assert isinstance(spec, ModuleSpec)
    module = importlib.util.module_from_spec(spec)
    assert isinstance(spec.loader, Loader)
    spec.loader.exec_module(module)

    return module
