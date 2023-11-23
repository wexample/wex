from typing import Union, Dict, List, Optional, Any, Literal, Callable

AddonNameType = Literal[
    'app',
    'core',
    'default',
    'docker',
    'service_db',
    'service_php',
    'service_various',
    'system',
    'test'
]

StringKeysDict = Dict[str, Any]
AnyCallable = Callable[..., Any]
KeyPairCommandArgs = Dict[str, Union[str, bool]]
Kwargs = StringKeysDict
StringMessageParameters = StringKeysDict
StringsDict = Dict[str, str]
RegistryAddon = Dict[Union['alias', 'command', 'file', 'properties', 'test'], StringsDict]
RegistryService = Dict[Union['addon', 'commands', 'config', 'dir', 'name'], StringsDict]
RegistryResolver = Dict[str, StringKeysDict | List[StringKeysDict]]
WritableFileContent = str | int | float | bool | None

KernelRegistry = Dict[
    Literal['env', 'resolvers'],
    str | Dict[str, RegistryResolver]
]

CoreCommandArgsDict = KeyPairCommandArgs
CoreCommandArgsList = List[str]
CoreCommandArgsListOrDict = Union[KeyPairCommandArgs, CoreCommandArgsList]
CoreCommandString = str
CoreCommandStringParts = List[str]

OptionalKeyPairCommandArgs = Optional[KeyPairCommandArgs]
OptionalCoreCommandArgsDict = Optional[CoreCommandArgsDict]
OptionalCoreCommandArgsListOrDict = Optional[CoreCommandArgsListOrDict]
