import os
from typing import Callable

from src.const.types import AnyCallable
from src.core.file.AbstractFileSystemStructure import AbstractFileSystemStructure


class DirectoryStructure(AbstractFileSystemStructure):
    type = "dir"

    def __init__(self, path: str, initialize: bool = True) -> None:
        if not path.endswith(os.sep):
            path += os.sep

        super().__init__(path, initialize)

    def create_missing(self) -> None:
        os.makedirs(self.path, exist_ok=True)

    def get_parent_dir(self) -> str:
        return os.path.dirname(os.path.dirname(self.path)) + os.path.sep

    def process_schema_recursive(
        self,
        action_function: AnyCallable,
    ) -> None:
        self._process_schema_recursive(
            item_name="",
            schema=self.get_schema(),
            action_function=action_function
        )

    def _process_schema_recursive(
        self,
        item_name: str,
        schema: dict,
        action_function: AnyCallable,
    ) -> None:
        action_function(item_name, schema)

        if "schema" in schema:
            for child_item_name, child_schema in schema["schema"].items():
                self._process_schema_recursive(
                    item_name=os.path.join(item_name, child_item_name),
                    schema=child_schema,
                    action_function=action_function,
                )
