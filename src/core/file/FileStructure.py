import os
from typing import Optional, Any

from src.const.types import WritableFileContent
from src.helper.file import file_create_parent_and_touch, file_read, file_write
from src.core.file.AbstractFileSystemStructure import AbstractFileSystemStructure, FILE_SYSTEM_TYPE_FILE, \
    FILE_SYSTEM_ERROR_WRONG_EXTENSION


class FileStructure(AbstractFileSystemStructure):
    type: str = FILE_SYSTEM_TYPE_FILE
    file_extension: Optional[str] = None
    content: Any

    def __init__(self,
                 path: str,
                 initialize: bool = True) -> None:
        self.content = None

        super().__init__(
            path=path,
            initialize=initialize
        )

    def checkup(self):
        super().checkup()

        if self.file_extension:
            _, extension = os.path.splitext(self.path)

            extension = extension[1:]

            if extension.lower() != self.file_extension.lower():
                self.add_error(
                    FILE_SYSTEM_ERROR_WRONG_EXTENSION,
                    {
                        'path': self.path,
                        'expected': self.file_extension
                    }
                )

    def load_content(self) -> Any:
        return file_read(self.path)

    def write_content(self) -> Any:
        return file_write(
            self.path,
            self.get_writable_content())

    def get_writable_content(self) -> WritableFileContent:
        return str(self.content)

    def create_missing(self):
        file_create_parent_and_touch(
            self.path
        )
