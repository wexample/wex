import os.path
from abc import ABC
from typing import Dict, Any, Literal, List, Optional
from abc import abstractmethod

from src.const.types import StringMessageParameters
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.ErrorMessage import ErrorMessage, ErrorMessageList

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
FILE_SYSTEM_SCHEMA_ITEM_KEY_SHORTCUT = 'shortcut'
FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST = 'should_exist'
FILE_SYSTEM_SCHEMA_ITEM_KEY_TYPE = 'type'

FileSystemStructureSchemaItemKeys = Literal[
    FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING,
    FILE_SYSTEM_SCHEMA_ITEM_KEY_SCHEMA,
    FILE_SYSTEM_SCHEMA_ITEM_KEY_SHORTCUT,
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
    children: Dict[str, Any]
    path: str
    type: FileSystemStructureType
    errors: 'ErrorMessageList'
    on_missing: str = FILE_SYSTEM_ACTION_ON_MISSING_ERROR
    schema: FileSystemStructureSchema = {}
    parent_structure: Optional['AbstractFileSystemStructure'] = None
    shortcut: Optional[str] = None
    shortcuts: Dict[str, 'AbstractFileSystemStructure']

    def __init__(self,
                 path: str,
                 initialize: bool = True) -> None:
        self.path = path
        self.errors = []
        self.children = {}
        self.shortcuts = {}

        if initialize:
            self.initialize()

    def initialize(self):
        self.load_schema()
        self.checkup()

    def set_parent(self, parent_structure: Optional['AbstractFileSystemStructure']):
        self.parent_structure = parent_structure

        if self.shortcut:
            self.parent_structure.set_shortcut(
                self.shortcut,
                self
            )

    def set_shortcut(self, name: str, structure: 'AbstractFileSystemStructure') -> None:
        self.shortcuts[name] = structure
        if self.parent_structure:
            self.parent_structure.set_shortcut(
                name,
                structure
            )

    def load_schema(self) -> None:
        for item_name in self.schema:
            options: FileSystemStructureSchemaItem = self.schema[item_name]

            type: str = options[
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
                initialize=False,
            )

            self.children[item_name] = structure
            structure.load_options(options)
            structure.set_parent(self)

            # Init after options loaded
            structure.initialize()

    def load_options(self, options: FileSystemStructureSchemaItem):
        if FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING in options:
            self.on_missing = options[FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING]

        if FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST in options:
            self.should_exist = bool(options[FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST])

        if FILE_SYSTEM_SCHEMA_ITEM_KEY_SHORTCUT in options:
            self.shortcut = str(options[FILE_SYSTEM_SCHEMA_ITEM_KEY_SHORTCUT])

        if FILE_SYSTEM_SCHEMA_ITEM_KEY_SCHEMA in options:
            self.schema = options[FILE_SYSTEM_SCHEMA_ITEM_KEY_SCHEMA]

        if self.on_missing:
            self.should_exist = True

    def checkup(self) -> None:
        if not self.exists():
            if self.should_exist is True:
                if self.on_missing == FILE_SYSTEM_ACTION_ON_MISSING_CREATE:
                    self.create_missing()
                elif self.on_missing == FILE_SYSTEM_ACTION_ON_MISSING_ERROR:
                    self.add_error(
                        FILE_SYSTEM_ERROR_NOT_FOUND,
                        {'path': self.path}
                    )

    def exists(self) -> bool:
        return os.path.exists(self.path)

    @abstractmethod
    def create_missing(self):
        pass

    def add_error(self, code: str, parameters: StringMessageParameters) -> 'ErrorMessage':
        from src.core.ErrorMessage import ErrorMessage

        error = ErrorMessage(
            code=code,
            parameters=parameters,
            message=FILE_SYSTEM_ERROR_MESSAGES[code]
        )

        self.errors.append(error)

        return error

    def get_all_errors(self) -> 'ErrorMessageList':
        errors = self.errors.copy()

        for children in self.children:
            errors += self.children[children].get_all_errors()

        return errors
