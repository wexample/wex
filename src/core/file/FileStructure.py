import os
from typing import Optional

from src.const.types import BasicValue
from src.core.file.AbstractFileSystemStructure import (
    FILE_SYSTEM_ERROR_WRONG_EXTENSION,
    AbstractFileSystemStructure, FileSystemStructureSchemaItem,
)
from src.helper.file import file_create_parent_and_touch, file_read, file_write


class FileStructure(AbstractFileSystemStructure):
    type = "file"
    file_extension: Optional[str] = None
    content: BasicValue
    default_content: str = ""

    def __init__(self, path: str, initialize: bool = True) -> None:
        self.content = None

        super().__init__(path=path, initialize=initialize)

    def checkup(self) -> None:
        super().checkup()

        if self.file_extension:
            _, extension = os.path.splitext(self.path)

            extension = extension[1:]

            if extension.lower() != self.file_extension.lower():
                self.add_error(
                    FILE_SYSTEM_ERROR_WRONG_EXTENSION,
                    {"path": self.path, "expected": self.file_extension},
                )

    def load_content(self) -> None:
        self.content = file_read(self.path)

    def load_options(self, options: FileSystemStructureSchemaItem) -> None:
        super().load_options(options)

        if "default_content" in options:
            self.default_content = str(options["default_content"])

    def write_content(self) -> None:
        file_write(self.path, str(self.get_writable_content()))

    def get_writable_content(self) -> BasicValue:
        return self.content

    def create_missing(self) -> None:
        file_create_parent_and_touch(
            self.path,
            self.default_content)
