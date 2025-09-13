from __future__ import annotations

from collections.abc import Callable, Mapping
from re import Match
from typing import (
    Any,
    Literal,
    Optional,
    TypedDict,
    Union,
)

AddonNameType = Literal[
    "app",
    "core",
    "default",
    "docker",
    "service_db",
    "service_php",
    "service_various",
    "system",
    "test",
]

AnyList = list[Any]

StringKeysDict = dict[str, Any]
StringKeysMapping = Mapping[str, Any]
StringsDict = dict[str, str]
StringsList = list[str]
SetList = set[str]
StringsMatch = Match[str]
BasicInlineValue = str | int | float | bool | None
BasicValue = BasicInlineValue | AnyList | StringKeysDict
JsonContent = BasicValue
JsonContentDict = StringKeysDict
YamlContent = BasicValue
YamlContentDict = StringKeysDict


AnyCallable = Callable[..., Any]
Args = Any
DecoratedCallable = Callable[..., AnyCallable]
Kwargs = Any
ResponsePrintType = Optional[BasicInlineValue | StringKeysDict | AnyList]
StringMessageParameters = StringKeysDict

CoreCommandArgsDict = Mapping[str, BasicInlineValue]
CoreCommandArgsList = StringsList
CoreCommandCommaSeparatedList = Union[str, StringsList]
CoreCommandArgsListOrDict = Union[StringKeysDict, CoreCommandArgsList]
CoreCommandString = str
CoreCommandStringParts = StringsList

OptionalCoreCommandArgsDict = Optional[CoreCommandArgsDict]
OptionalCoreCommandArgsListOrDict = Optional[CoreCommandArgsListOrDict]

AppConfigValue = BasicValue
AppDockerEnvConfig = dict[str, AppConfigValue]
AppsPathsList = StringsDict

ShellCommandsList = StringsList
ShellCommandsDeepList = list[str | ShellCommandsList]
ShellCommandResponseTuple = tuple[bool, StringsList]

FileSystemStructureType = Literal[
    "file",
    "dir",
]


class FileSystemStructureSchemaItem(TypedDict, total=False):
    class_name: str | None
    default_content: str | None
    group: str | None
    on_missing: str | None
    permissions: int | None
    schema: FileSystemStructureSchema | None
    shortcut: str | None
    should_exist: bool | None
    type: FileSystemStructureType
    remote: str | None
    user: str | None


class FileSystemStructurePermission(TypedDict):
    mode: int
    recursive: bool


FileSystemStructureSchema = StringKeysDict


class RegistryCommand(TypedDict):
    alias: str
    attachments: StringsDict
    command: str
    file: str
    properties: StringsDict
    test: str


RegistryCommandsCollection = dict[str, RegistryCommand]


class RegistryService(TypedDict):
    addon: str
    commands: RegistryCommandsCollection
    config: StringKeysDict
    dir: str
    name: str


class RegistryAddon(TypedDict):
    commands: RegistryCommandsCollection
    name: str


RegistryAllServices = dict[str, RegistryService]
RegistryResolverData = StringKeysDict


class YamlCommandScript(TypedDict):
    command: str | None
    container_name: str | None
    directory: str | None
    file: str | None
    interpreter: StringsList
    options: StringKeysDict | None
    script: str | None
    sync: bool
    title: str
    type: str
    variable: str


class YamlCommandOption(TypedDict):
    default: str | bool | int
    help: str
    is_flag: bool
    name: str
    required: bool
    short: str
    type: str


class YamlCommand(TypedDict):
    attach: StringKeysDict | None
    help: str
    name: str
    options: list[YamlCommandOption]
    scripts: list[YamlCommandScript]
    type: str


class AppConfig(TypedDict):
    branch: str | None
    domain_main: str
    domain_tld: str
    domains: list[str]
    domains_string: str
    env: StringKeysDict
    name: str
    host: dict[str, str]
    password: dict[str, str]
    path: dict[str, str]
    server: StringKeysDict
    service: StringKeysDict
    started: bool
    structure: FileSystemStructureSchema
    user: dict[str, str | int]


class AppRuntimeConfig(TypedDict):
    branch: str | None
    domain_main: str
    domain_tld: str
    domains: list[str]
    domains_string: str
    env: str
    name: str
    host: dict[str, str]
    password: dict[str, str]
    path: dict[str, str]
    server: StringKeysDict
    service: StringKeysDict
    started: bool
    structure: FileSystemStructureSchema
    user: dict[str, str | int]


AnyAppConfig = Union[AppConfig | AppRuntimeConfig]


class DockerCompose(TypedDict):
    services: Any


class KernelRegistry(StringKeysDict):
    env: str
    resolvers: dict[str, RegistryResolverData]

    def __init__(self, env: str, resolvers: StringKeysDict | None = None) -> None:
        super().__init__()
        self.env = env
        self.resolvers = resolvers or {}

    def to_dict(self) -> StringKeysDict:
        return vars(self)


class VersionDescriptor(TypedDict):
    major: int | None
    intermediate: int | None
    minor: int | None
    pre_build_type: str | None
    pre_build_number: int | None
