import os.path
from abc import ABC
from typing import Dict, Any, Literal, List

FILE_SYSTEM_TYPE_FILE: str = 'file'
FILE_SYSTEM_TYPE_DIR: str = 'dir'

FILE_SYSTEM_ERROR_NOT_FOUND: str = 'FILE_SYSTEM_ERROR_NOT_FOUND'
FILE_SYSTEM_ERROR_MESSAGES: Dict[str, str] = {
    FILE_SYSTEM_ERROR_NOT_FOUND: 'File or directory not found : {path}'
}

FileSystemStructureErrorItem = Dict[str, str | Dict[str, Any]]
FileSystemStructureSchema = Dict[str, Dict[str, Any]]
FileSystemStructureType = Literal[
    FILE_SYSTEM_TYPE_FILE,
    FILE_SYSTEM_TYPE_DIR,
]


class AbstractFileSystemStructure(ABC):
    should_exist: bool = False
    checkup: bool = False
    children: Dict[str, Any] = {}
    path: str
    type: FileSystemStructureType
    errors: List[FileSystemStructureErrorItem]

    def __init__(self, path: str) -> None:
        self.path = path

        if self.checkup:
            if not os.path.exists(self.path):
                self.add_error(
                    FILE_SYSTEM_ERROR_NOT_FOUND,
                    {'path': self.path}
                )

    def add_error(self, code, data):
        self.errors.append({
            'code': code,
            'data': data,
            'message': FILE_SYSTEM_ERROR_MESSAGES[code]
        })
