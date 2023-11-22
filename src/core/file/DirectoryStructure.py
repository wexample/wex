import os

from src.core.file.AbstractFileSystemStructure import AbstractFileSystemStructure, FILE_SYSTEM_TYPE_DIR


class DirectoryStructure(AbstractFileSystemStructure):
    type: str = FILE_SYSTEM_TYPE_DIR

    def __init__(self,
                 path: str,
                 allow_initial_checkup: bool = True) -> None:
        if not path.endswith(os.sep):
            path += os.sep
            
        super().__init__(
            path,
            allow_initial_checkup)

    def create_missing(self):
        os.makedirs(
            self.path,
            exist_ok=True
        )
