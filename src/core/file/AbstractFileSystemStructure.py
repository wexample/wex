import os.path
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Optional, cast

from wexample_helpers.helpers.file import file_change_mode_recursive

from src.const.types import (
    FileSystemStructurePermission,
    FileSystemStructureSchema,
    FileSystemStructureSchemaItem,
    FileSystemStructureType,
    StringMessageParameters,
)
from src.core.BaseClass import BaseClass
from src.helper.user import set_owner_recursively

if TYPE_CHECKING:
    from src.core.ErrorMessage import ErrorMessage, ErrorMessageList

FILE_SYSTEM_ACTION_ON_MISSING_ERROR = "error"
FILE_SYSTEM_ACTION_ON_MISSING_CREATE = "create"

FILE_SYSTEM_ERROR_NOT_FOUND: str = "FILE_SYSTEM_ERROR_NOT_FOUND"
FILE_SYSTEM_ERROR_WRONG_EXTENSION: str = "FILE_SYSTEM_ERROR_WRONG_EXTENSION"
FILE_SYSTEM_ERROR_MESSAGES: Dict[str, str] = {
    FILE_SYSTEM_ERROR_NOT_FOUND: "File or directory not found : {path}",
    FILE_SYSTEM_ERROR_WRONG_EXTENSION: "Wrong file extension for file {path}, expected {expected}",
}


class AbstractFileSystemStructure(BaseClass):
    should_exist: Optional[bool] = True
    children: Dict[str, Any]
    path: str
    type: FileSystemStructureType
    errors: "ErrorMessageList"
    group: Optional[str] = None
    on_missing: str = FILE_SYSTEM_ACTION_ON_MISSING_ERROR
    parent_structure: Optional["AbstractFileSystemStructure"] = None
    permissions: Optional[FileSystemStructurePermission] = None
    shortcut: Optional[str] = None
    shortcuts: Dict[str, "AbstractFileSystemStructure"]
    user: Optional[str] = None

    def __init__(self, path: str, initialize: bool = True) -> None:
        self.path = path
        self.errors = []
        self.children = {}
        self.shortcuts = {}
        self.schema: FileSystemStructureSchema = {}

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

    def get_schema(self) -> FileSystemStructureSchema:
        return self.schema

    def load_schema(self) -> None:
        root_schema = self.get_schema()

        if "schema" in root_schema:
            schema = root_schema["schema"]

            for item_name in schema:
                options: FileSystemStructureSchemaItem = schema[item_name]

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
        if "group" in options:
            self.group = options["group"]

        if "on_missing" in options:
            self.on_missing = str(options["on_missing"])

        if "permissions" in options:
            if isinstance(options["permissions"], dict):
                permissions = cast(
                    FileSystemStructurePermission, options["permissions"]
                )
            else:
                permissions = cast(
                    FileSystemStructurePermission,
                    {"mode": options["permissions"], "recursive": False},
                )

            permissions["mode"] = int(permissions["mode"] or 644)
            self.permissions = permissions

        if "should_exist" in options:
            self.should_exist = bool(options["should_exist"])

        if "shortcut" in options:
            self.shortcut = str(options["shortcut"])

        if "schema" in options:
            self.schema = {"schema": options["schema"]} or {}

        if "user" in options:
            self.user = options["user"]

    def checkup(self) -> None:
        if not self.exists():
            if self.should_exist is True:
                if self.on_missing == FILE_SYSTEM_ACTION_ON_MISSING_CREATE:
                    self.create_missing()
                elif self.on_missing == FILE_SYSTEM_ACTION_ON_MISSING_ERROR:
                    self.add_error(FILE_SYSTEM_ERROR_NOT_FOUND, {"path": self.path})

        if self.permissions:
            file_change_mode_recursive(self.path, self.permissions["mode"])

        if self.user:
            set_owner_recursively(
                self.path,
                self.user,
                self.group,
            )

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
