import os.path
from abc import ABC
from typing import Dict, Any, Literal, List, Optional
from abc import abstractmethod

FILE_SYSTEM_TYPE_FILE: str = 'file'
FILE_SYSTEM_TYPE_DIR: str = 'dir'

FILE_SYSTEM_ACTION_ON_MISSING_ERROR = 'error'
FILE_SYSTEM_ACTION_ON_MISSING_CREATE = 'create'

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
    should_exist: Optional[bool] = None
    initial_checkup: bool = True
    children: Dict[str, Any] = {}
    path: str
    type: FileSystemStructureType
    errors: List[FileSystemStructureErrorItem]
    on_missing: str

    def __init__(self, path: str) -> None:
        self.path = path
        self.errors = []

        if self.initial_checkup:
            self.checkup()

    def checkup(self):
        if not os.path.exists(self.path):
            if self.should_exist is True:
                if self.on_missing == FILE_SYSTEM_ACTION_ON_MISSING_CREATE:
                    self.create_missing()
                elif self.on_missing == FILE_SYSTEM_ACTION_ON_MISSING_ERROR:
                    self.add_error(
                        FILE_SYSTEM_ERROR_NOT_FOUND,
                        {'path': self.path}
                    )

    @abstractmethod
    def create_missing(self):
        pass

    def add_error(self, code, data):
        self.errors.append({
            'code': code,
            'data': data,
            'message': FILE_SYSTEM_ERROR_MESSAGES[code]
        })
