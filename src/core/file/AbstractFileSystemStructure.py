import os.path
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, TypedDict

from src.const.types import StringMessageParameters
from src.core.BaseClass import BaseClass

if TYPE_CHECKING:
    from src.core.ErrorMessage import ErrorMessage, ErrorMessageList

FileSystemStructureType = Literal[
    "file",
    "dir",
]

FILE_SYSTEM_ACTION_ON_MISSING_ERROR = "error"
FILE_SYSTEM_ACTION_ON_MISSING_CREATE = "create"

FILE_SYSTEM_ERROR_NOT_FOUND: str = "FILE_SYSTEM_ERROR_NOT_FOUND"
FILE_SYSTEM_ERROR_WRONG_EXTENSION: str = "FILE_SYSTEM_ERROR_WRONG_EXTENSION"
FILE_SYSTEM_ERROR_MESSAGES: Dict[str, str] = {
    FILE_SYSTEM_ERROR_NOT_FOUND: "File or directory not found : {path}",
    FILE_SYSTEM_ERROR_WRONG_EXTENSION: "Wrong file extension for file {path}, expected {expected}",
}


class FileSystemStructureSchemaItem(TypedDict, total=False):
    class_name: Optional[str]
    on_missing: Optional[str]
    schema: Optional["FileSystemStructureSchema"]
    shortcut: Optional[str]
    should_exist: Optional[bool]
    type: FileSystemStructureType


FileSystemStructureSchema = Dict[str, FileSystemStructureSchemaItem]


class AbstractFileSystemStructure(BaseClass):
    should_exist: Optional[bool] = True
    children: Dict[str, Any]
    path: str
    type: FileSystemStructureType
    errors: "ErrorMessageList"
    on_missing: str = FILE_SYSTEM_ACTION_ON_MISSING_ERROR
    schema: FileSystemStructureSchema = {}
    parent_structure: Optional["AbstractFileSystemStructure"] = None
    shortcut: Optional[str] = None
    shortcuts: Dict[str, "AbstractFileSystemStructure"]

    def __init__(self, path: str, initialize: bool = True) -> None:
        self.path = path
        self.errors = []
        self.children = {}
        self.shortcuts = {}

        if initialize:
            self.initialize()

    def initialize(self) -> None:
        self.load_schema()
        self.checkup()

    def set_parent(self, parent_structure: "AbstractFileSystemStructure") -> None:
        self.parent_structure = parent_structure

        if self.shortcut:
            parent_structure.set_shortcut(self.shortcut, self)

    def set_shortcut(self, name: str, structure: "AbstractFileSystemStructure") -> None:
        self.shortcuts[name] = structure
        if self.parent_structure:
            self.parent_structure.set_shortcut(name, structure)

    def load_schema(self) -> None:
        for item_name in self.schema:
            options: FileSystemStructureSchemaItem = self.schema[item_name]

            type: str = options["type"] if "type" in options else "dir"
            class_definition: Any = (
                options["class_name"] if "class_name" in options else None
            )

            if class_definition is None:
                if type == "file":
                    from src.core.file.FileStructure import FileStructure

                    class_definition = FileStructure
                    assert class_definition is FileStructure
                else:
                    from src.core.file.DirectoryStructure import DirectoryStructure

                    class_definition = DirectoryStructure
                    assert class_definition is DirectoryStructure

            structure: AbstractFileSystemStructure = class_definition(
                path=os.path.join(self.path, item_name),
                initialize=False,
            )

            self.children[item_name] = structure
            structure.load_options(options)
            structure.set_parent(self)

            # Init after options loaded
            structure.initialize()

    def load_options(self, options: FileSystemStructureSchemaItem) -> None:
        if "on_missing" in options:
            self.on_missing = str(options["on_missing"])

        if "should_exist" in options:
            self.should_exist = bool(options["should_exist"])

        if "shortcut" in options:
            self.shortcut = str(options["shortcut"])

        if "schema" in options:
            self.schema = options["schema"] or {}

        if self.on_missing:
            self.should_exist = True

    def checkup(self) -> None:
        if not self.exists():
            if self.should_exist is True:
                if self.on_missing == FILE_SYSTEM_ACTION_ON_MISSING_CREATE:
                    self.create_missing()
                elif self.on_missing == FILE_SYSTEM_ACTION_ON_MISSING_ERROR:
                    self.add_error(FILE_SYSTEM_ERROR_NOT_FOUND, {"path": self.path})

    def exists(self) -> bool:
        return os.path.exists(self.path)

    @abstractmethod
    def create_missing(self) -> None:
        pass

    def add_error(
        self, code: str, parameters: StringMessageParameters
    ) -> "ErrorMessage":
        from src.core.ErrorMessage import ErrorMessage

        error = ErrorMessage(
            code=code, parameters=parameters, message=FILE_SYSTEM_ERROR_MESSAGES[code]
        )

        self.errors.append(error)

        return error

    def get_all_errors(self) -> "ErrorMessageList":
        errors = self.errors.copy()

        for children in self.children:
            errors += self.children[children].get_all_errors()

        return errors
