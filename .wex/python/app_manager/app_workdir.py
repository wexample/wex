from __future__ import annotations

from wexample_config.const.types import DictConfig
from wexample_filestate.const.disk import DiskItemType
from wexample_wex_addon_dev_python.workdir.python_workdir import PythonWorkdir


class AppWorkdir(PythonWorkdir):
    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        raw_value = super().prepare_value(raw_value=raw_value)

        raw_value.get("children").extend([
            {
                "name": "src",
                "type": DiskItemType.DIRECTORY,
                "should_exist": True,
                "children": [
                    self._create_init_children_factory(),
                    self._create_python_file_children_filter(),
                    {
                        "name": "py.typed",
                        "type": DiskItemType.FILE,
                        "should_exist": True,
                    },
                ],
            }]
        )

        return raw_value
