from src.core.file.AbstractFileSystemStructure import AbstractFileSystemStructure, FILE_SYSTEM_TYPE_DIR


class DirectoryStructure(AbstractFileSystemStructure):
    type: str = FILE_SYSTEM_TYPE_DIR
