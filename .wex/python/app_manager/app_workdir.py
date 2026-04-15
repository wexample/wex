from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_wex_addon_dev_python.workdir.python_workdir import PythonWorkdir

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class AppWorkdir(PythonWorkdir):
    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        raw_value = super().prepare_value(raw_value=raw_value)

        # wex is a CLI app, not a standard Python package — it does not follow
        # the src/{vendor}_{name}/ layout enforced by PythonWorkdir.
        raw_value["children"] = [
            child
            for child in raw_value["children"]
            if not (isinstance(child, dict) and child.get("name") == "src")
        ]

        return raw_value

    def get_package_import_name(self) -> str:
        return "wex"

    def get_package_name(self) -> str:
        return "wex"
