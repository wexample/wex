from typing import Any, Callable, Dict, List, Literal, Optional, TypedDict, Union

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
StringsList = List[str]
BasicInlineValue = str | int | float | bool | None
BasicValue = BasicInlineValue | AnyList | StringKeysDict
JsonContent = Optional[BasicInlineValue | StringKeysDict]
YamlContent = Optional[BasicInlineValue | StringKeysDict]
YamlContentDict = StringKeysDict

AnyCallable = Callable[..., Any]
Args = AnyList
DecoratedCallable = Callable[..., Callable[..., Any]]
Kwargs = Any
ResponsePrintType = Optional[BasicInlineValue | StringKeysDict | AnyList]
StringMessageParameters = StringKeysDict
StringsDict = Dict[str, str]

CoreCommandArgsDict = Dict[str, BasicInlineValue]
CoreCommandArgsList = StringsList
CoreCommandArgsListOrDict = Union[StringKeysDict, CoreCommandArgsList]
CoreCommandString = str
CoreCommandStringParts = StringsList

OptionalCoreCommandArgsDict = Optional[CoreCommandArgsDict]
OptionalCoreCommandArgsListOrDict = Optional[CoreCommandArgsListOrDict]

AppConfigValue = BasicValue
AppDockerEnvConfig = Dict[str, AppConfigValue]
AppsPathsList = StringsDict
ShellCommandsList = StringsList


class RegistryCommand(TypedDict):
    alias: str
    command: str
    file: str
    properties: StringsDict
    test: str


RegistryCommandsCollection = Dict[str, RegistryCommand]


class RegistryService(TypedDict):
    addon: str
    commands: RegistryCommandsCollection
    config: str
    dir: str
    name: str


class RegistryAddon(TypedDict):
    commands: RegistryCommandsCollection
    name: str


RegistryAllServices = Dict[str, RegistryService]
RegistryResolverData = StringKeysDict


class YamlCommandScript(TypedDict):
    container_name: Optional[str]
    file: Optional[str]
    interpreter: StringsList
    script: Optional[str]
    title: str
    type: str


class YamlCommandOption(TypedDict):
    default: str | bool | int
    help: str
    is_flag: bool
    name: str
    required: bool
    short: str
    type: str


class YamlCommand(TypedDict):
    help: str
    name: str
    options: List[YamlCommandOption]
    scripts: List[YamlCommandScript]
    type: str


class AppConfig(TypedDict):
    domain_main: str
    domain_tld: str
    domains: List[str]
    domains_string: str
    env: Dict[str, Any]
    name: str
    host: Dict[str, str]
    password: Dict[str, str]
    path: Dict[str, str]
    service: Dict[str, Any]
    started: bool
    user: Dict[str, str | int]


class AppRuntimeConfig(TypedDict):
    domain_main: str
    domain_tld: str
    domains: List[str]
    domains_string: str
    env: str
    name: str
    host: Dict[str, str]
    password: Dict[str, str]
    path: Dict[str, str]
    service: Dict[str, Any]
    started: bool
    user: Dict[str, str | int]


AnyAppConfig = Union[AppConfig | AppRuntimeConfig]


class DockerCompose(TypedDict):
    services: Any


class KernelRegistry(StringKeysDict):
    env: Optional[str]
    resolvers: Dict[str, RegistryResolverData]

    def __init__(
        self, env: Optional[str] = None, resolvers: Optional[StringKeysDict] = None
    ) -> None:
        super().__init__()
        self.env = env
        self.resolvers = resolvers or {}

    def to_dict(self) -> StringKeysDict:
        return vars(self)
