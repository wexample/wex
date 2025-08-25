from typing import Optional

from wexample_config.const.types import DictConfig
from wexample_filestate_python.workdir.python_workdir import PythonWorkdir


class WexWorkdir(PythonWorkdir):
    def prepare_value(self, raw_value: Optional[DictConfig] = None) -> DictConfig:
        from wexample_filestate.const.disk import DiskItemType

        raw_value = super().prepare_value(
            raw_value=raw_value
        )

        children = raw_value["children"]
        children.extend(
            [
                {
                    "name": "addons",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_init_children_factory(),
                        self._create_python_file_children_filter(),
                    ],
                },
                {
                    "name": "src",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_init_children_factory(),
                        self._create_python_file_children_filter(),
                    ],
                },
                {
                    "name": "tests",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_init_children_factory(),
                        self._create_python_file_children_filter(),
                    ],
                }
            ]
        )

        return raw_value
