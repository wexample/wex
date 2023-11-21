from typing import Union, Dict, List, Optional

KeyPairCommandArgs = Dict[str, Union[str, bool]]
StringsKeyPair = Dict[str, str]

CoreCommandArgsDict = KeyPairCommandArgs
CoreCommandArgsListOrDict = Union[KeyPairCommandArgs, List[str]]
CoreCommandString = str
CoreCommandStringParts = List[str]

OptionalKeyPairCommandArgs = Optional[KeyPairCommandArgs]
OptionalCoreCommandArgsDict = Optional[CoreCommandArgsDict]
OptionalCoreCommandArgsListOrDict = Optional[CoreCommandArgsListOrDict]
