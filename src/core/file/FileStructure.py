import os
from typing import Optional

from src.helper.file import file_create_parent_and_touch
from src.core.file.AbstractFileSystemStructure import AbstractFileSystemStructure, FILE_SYSTEM_TYPE_FILE, \
    FILE_SYSTEM_ERROR_WRONG_EXTENSION


class FileStructure(AbstractFileSystemStructure):
    type: str = FILE_SYSTEM_TYPE_FILE
    file_extension: Optional[str] = None

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

    def create_missing(self):
        file_create_parent_and_touch(
            self.path
        )
