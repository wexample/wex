from typing import Union, Dict, List, Optional

KeyPairCommandArgs = Dict[str, Union[str, bool]]
StringsKeyPair = Dict[str, str]

CoreCommandArgsDict = KeyPairCommandArgs
CoreCommandArgsList = List[str]
CoreCommandArgsListOrDict = Union[KeyPairCommandArgs, CoreCommandArgsList]
CoreCommandString = str
CoreCommandStringParts = List[str]

OptionalKeyPairCommandArgs = Optional[KeyPairCommandArgs]
OptionalCoreCommandArgsDict = Optional[CoreCommandArgsDict]
OptionalCoreCommandArgsListOrDict = Optional[CoreCommandArgsListOrDict]
