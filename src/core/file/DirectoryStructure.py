import os

from src.core.file.AbstractFileSystemStructure import (
    FILE_SYSTEM_TYPE_DIR,
    AbstractFileSystemStructure,
)


class DirectoryStructure(AbstractFileSystemStructure):
    type: str = FILE_SYSTEM_TYPE_DIR

    def __init__(self, path: str, initialize: bool = True) -> None:
        if not path.endswith(os.sep):
            path += os.sep

        super().__init__(path, initialize)

    def create_missing(self):
        os.makedirs(self.path, exist_ok=True)
