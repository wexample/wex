import os

from src.core.file.AbstractFileSystemStructure import AbstractFileSystemStructure


class DirectoryStructure(AbstractFileSystemStructure):
    type = "dir"

    def __init__(self, path: str, initialize: bool = True) -> None:
        if not path.endswith(os.sep):
            path += os.sep

        super().__init__(path, initialize)

    def create_missing(self) -> None:
        os.makedirs(self.path, exist_ok=True)
