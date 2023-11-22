import os.path
from abc import ABC
from typing import Dict, Any, Literal, List, Optional
from abc import abstractmethod

from src.const.types import StringMessageParameters

FILE_SYSTEM_TYPE_FILE: str = 'file'
FILE_SYSTEM_TYPE_DIR: str = 'dir'

FILE_SYSTEM_ACTION_ON_MISSING_ERROR = 'error'
FILE_SYSTEM_ACTION_ON_MISSING_CREATE = 'create'

FILE_SYSTEM_ERROR_NOT_FOUND: str = 'FILE_SYSTEM_ERROR_NOT_FOUND'
FILE_SYSTEM_ERROR_WRONG_EXTENSION: str = 'FILE_SYSTEM_ERROR_WRONG_EXTENSION'
FILE_SYSTEM_ERROR_MESSAGES: Dict[str, str] = {
    FILE_SYSTEM_ERROR_NOT_FOUND: 'File or directory not found : {path}',
    FILE_SYSTEM_ERROR_WRONG_EXTENSION: 'Wrong file extension for file {path}, expected {expected}'
}

FILE_SYSTEM_SCHEMA_ITEM_KEY_CLASS = 'class'
FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING = 'on_missing'
FILE_SYSTEM_SCHEMA_ITEM_KEY_SCHEMA = 'schema'
FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST = 'should_exist'
FILE_SYSTEM_SCHEMA_ITEM_KEY_TYPE = 'type'

FileSystemStructureErrorItem = Dict[str, str | Dict[str, Any]]
FileSystemStructureSchemaItemKeys = Literal[
    FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING,
    FILE_SYSTEM_SCHEMA_ITEM_KEY_SCHEMA,
    FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST,
    FILE_SYSTEM_SCHEMA_ITEM_KEY_TYPE,
]
FileSystemStructureSchemaItem = Dict[FileSystemStructureSchemaItemKeys, str | Dict[str, Any]]
FileSystemStructureSchema = Dict[str, FileSystemStructureSchemaItem]
FileSystemStructureType = Literal[
    FILE_SYSTEM_TYPE_FILE,
    FILE_SYSTEM_TYPE_DIR,
]


class AbstractFileSystemStructure(ABC):
    should_exist: Optional[bool] = True
    initial_checkup: bool = True
    children: Dict[str, Any]
    path: str
    type: FileSystemStructureType
    errors: List[FileSystemStructureErrorItem]
    on_missing: str = FILE_SYSTEM_ACTION_ON_MISSING_ERROR
    schema: FileSystemStructureSchema = {}

    def __init__(self,
                 path: str,
                 allow_initial_checkup: bool = True) -> None:
        self.path = path
        self.errors = []
        self.children = {}
        self.create_children()

        if allow_initial_checkup and self.initial_checkup:
            self.checkup()

    def create_children(self):
        for item_name in self.schema:
            options = self.schema[item_name]
            type = options[
                FILE_SYSTEM_SCHEMA_ITEM_KEY_TYPE] if FILE_SYSTEM_SCHEMA_ITEM_KEY_TYPE in options else FILE_SYSTEM_TYPE_DIR
            class_definition: Any = options[
                FILE_SYSTEM_SCHEMA_ITEM_KEY_CLASS] if FILE_SYSTEM_SCHEMA_ITEM_KEY_CLASS in options else None

            if class_definition is None:
                if type == FILE_SYSTEM_TYPE_FILE:
                    from src.core.file.FileStructure import FileStructure
                    class_definition = FileStructure
                    assert class_definition is FileStructure
                else:
                    from src.core.file.DirectoryStructure import DirectoryStructure
                    class_definition = DirectoryStructure
                    assert class_definition is DirectoryStructure

            structure: AbstractFileSystemStructure = class_definition(
                path=os.path.join(
                    self.path,
                    item_name
                ),
                allow_initial_checkup=False
            )

            structure.load_options(options)

            self.children[item_name] = structure

            # Run checkup now than options are loaded.
            if structure.initial_checkup:
                structure.checkup()

    def load_options(self, options: FileSystemStructureSchemaItem):
        if options[FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING] \
                if FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING in options else None:
            self.on_missing = options[FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING]

        if options[FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST] \
                if FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST in options else None:
            self.should_exist = bool(options[FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST])

        if self.on_missing:
            self.should_exist = True

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

    def add_error(self, code: str, parameters: StringMessageParameters) -> None:
        self.errors.append({
            'code': code,
            'parameters': parameters,
            'message': FILE_SYSTEM_ERROR_MESSAGES[code]
        })

    def get_all_errors(self) -> List[FileSystemStructureErrorItem]:
        errors = self.errors.copy()

        for children in self.children:
            errors += self.children[children].get_all_errors()

        return errors
