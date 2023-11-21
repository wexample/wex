from typing import Union, Dict, List, Optional, Any, Literal

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

KeyPairCommandArgs = Dict[str, Union[str, bool]]
StringsKeyPair = Dict[str, str]
RegistryAddon = Dict[str, Dict[str, Any]]
RegistryService = Dict[str, Dict[str, Any]]

KernelRegistry = Dict[
    Literal[
        'addon',
        'env',
        'service',
    ],
    Dict[str, RegistryAddon] | str | Dict[str, RegistryService]
]

CoreCommandArgsDict = KeyPairCommandArgs
CoreCommandArgsList = List[str]
CoreCommandArgsListOrDict = Union[KeyPairCommandArgs, CoreCommandArgsList]
CoreCommandString = str
CoreCommandStringParts = List[str]

OptionalKeyPairCommandArgs = Optional[KeyPairCommandArgs]
OptionalCoreCommandArgsDict = Optional[CoreCommandArgsDict]
OptionalCoreCommandArgsListOrDict = Optional[CoreCommandArgsListOrDict]
