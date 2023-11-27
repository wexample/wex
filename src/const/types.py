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

AnyCallable = Callable[..., Any]
Args = AnyList
DecoratedCallable = Callable[..., Callable[..., Any]]
KeyPairCommandArgs = Dict[str, Union[str, bool]]
Kwargs = Any
StringMessageParameters = StringKeysDict
StringsDict = Dict[str, str]
RegistryAddon = Dict[
    Union["alias", "command", "file", "properties", "test"], StringsDict
]
RegistryService = Dict[Union["addon", "commands", "config", "dir", "name"], StringsDict]
RegistryResolverData = Dict[str, StringKeysDict | List[StringKeysDict]]
WritableFileContent = str | int | float | bool | None

CoreCommandArgsDict = KeyPairCommandArgs
CoreCommandArgsList = StringsList
CoreCommandArgsListOrDict = Union[StringKeysDict, CoreCommandArgsList]
CoreCommandString = str
CoreCommandStringParts = StringsList

OptionalKeyPairCommandArgs = Optional[KeyPairCommandArgs]
OptionalCoreCommandArgsDict = Optional[CoreCommandArgsDict]
OptionalCoreCommandArgsListOrDict = Optional[CoreCommandArgsListOrDict]

YamlContent = StringKeysDict

BasicArg = None | int | float | str | bool | AnyList | StringKeysDict
AppConfigValue = BasicArg
AppDockerEnvConfig = Dict[str, AppConfigValue]
AppsPathsList = StringsDict


class YamlCommandScript(TypedDict):
    title: str
    script: str
    file: str


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


class KernelRegistry(YamlContent):
    env: Optional[str]
    resolvers: Dict[str, RegistryResolverData]

    def __init__(self, resolvers: StringKeysDict, env: Optional[str] = None) -> None:
        super().__init__()
        self.env = env
        self.resolvers = resolvers
