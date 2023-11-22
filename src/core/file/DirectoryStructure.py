import os

from src.core.file.AbstractFileSystemStructure import AbstractFileSystemStructure, FILE_SYSTEM_TYPE_DIR


class DirectoryStructure(AbstractFileSystemStructure):
    type: str = FILE_SYSTEM_TYPE_DIR

    def create_missing(self):
        os.makedirs(
            self.path,
            exist_ok=True
        )
