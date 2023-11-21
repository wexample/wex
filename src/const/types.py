from typing import Union, Dict, List, Optional

KeyPairCommandArgs = Dict[str, Union[str, bool]]
StringsKeyPair = Dict[str, str]

CoreCommandArgsDict = KeyPairCommandArgs
CoreCommandArgsListOrDict = Union[KeyPairCommandArgs, List[str]]
CoreStringCommand = str

OptionalKeyPairCommandArgs = Optional[KeyPairCommandArgs]
OptionalCoreCommandDict = Optional[CoreCommandArgsDict]
OptionalCoreCommandArgsListOrDict = Optional[CoreCommandArgsListOrDict]
