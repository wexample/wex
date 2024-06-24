from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Mapping,
    Match,
    Optional,
    Set,
    Tuple,
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

AnyList = List[Any]

StringKeysDict = Dict[str, Any]
StringKeysMapping = Mapping[str, Any]
StringsDict = Dict[str, str]
StringsList = List[str]
SetList = Set[str]
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
AppDockerEnvConfig = Dict[str, AppConfigValue]
AppsPathsList = StringsDict

ShellCommandsList = StringsList
ShellCommandsDeepList = List[str | ShellCommandsList]
ShellCommandResponseTuple = Tuple[bool, StringsList]

FileSystemStructureType = Literal[
    "file",
    "dir",
]


class FileSystemStructureSchemaItem(TypedDict, total=False):
    class_name: Optional[str]
    default_content: Optional[str]
    group: Optional[str]
    on_missing: Optional[str]
    permissions: Optional[int]
    schema: Optional["FileSystemStructureSchema"]
    shortcut: Optional[str]
    should_exist: Optional[bool]
    type: FileSystemStructureType
    remote: Optional[str]
    user: Optional[str]


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


RegistryCommandsCollection = Dict[str, RegistryCommand]


class RegistryService(TypedDict):
    addon: str
    commands: RegistryCommandsCollection
    config: StringKeysDict
    dir: str
    name: str


class RegistryAddon(TypedDict):
    commands: RegistryCommandsCollection
    name: str


RegistryAllServices = Dict[str, RegistryService]
RegistryResolverData = StringKeysDict


class YamlCommandScript(TypedDict):
    command: Optional[str]
    container_name: Optional[str]
    directory: Optional[str]
    file: Optional[str]
    interpreter: StringsList
    options: Optional[StringKeysDict]
    script: Optional[str]
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
    attach: Optional[StringKeysDict]
    help: str
    name: str
    options: List[YamlCommandOption]
    scripts: List[YamlCommandScript]
    type: str


class AppConfig(TypedDict):
    branch: Optional[str]
    domain_main: str
    domain_tld: str
    domains: List[str]
    domains_string: str
    env: StringKeysDict
    name: str
    host: Dict[str, str]
    password: Dict[str, str]
    path: Dict[str, str]
    server: StringKeysDict
    service: StringKeysDict
    started: bool
    structure: FileSystemStructureSchema
    user: Dict[str, str | int]


class AppRuntimeConfig(TypedDict):
    branch: Optional[str]
    domain_main: str
    domain_tld: str
    domains: List[str]
    domains_string: str
    env: str
    name: str
    host: Dict[str, str]
    password: Dict[str, str]
    path: Dict[str, str]
    server: StringKeysDict
    service: StringKeysDict
    started: bool
    structure: FileSystemStructureSchema
    user: Dict[str, str | int]


AnyAppConfig = Union[AppConfig | AppRuntimeConfig]


class DockerCompose(TypedDict):
    services: Any


class KernelRegistry(StringKeysDict):
    env: str
    resolvers: Dict[str, RegistryResolverData]

    def __init__(self, env: str, resolvers: Optional[StringKeysDict] = None) -> None:
        super().__init__()
        self.env = env
        self.resolvers = resolvers or {}

    def to_dict(self) -> StringKeysDict:
        return vars(self)


class VersionDescriptor(TypedDict):
    major: Optional[int]
    intermediate: Optional[int]
    minor: Optional[int]
    pre_build_type: Optional[str]
    pre_build_number: Optional[int]
