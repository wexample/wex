from src.helper.file import file_create_parent_and_touch
from src.core.file.AbstractFileSystemStructure import AbstractFileSystemStructure, FILE_SYSTEM_TYPE_DIR


class FileStructure(AbstractFileSystemStructure):
    type: str = FILE_SYSTEM_TYPE_DIR

    def create_missing(self):
        file_create_parent_and_touch(
            self.path
        )
