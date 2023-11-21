from typing import Union, Dict, List, Optional

KeyPairCommandArgs = Dict[str, Union[str, bool]]
CommandArgs = Union[KeyPairCommandArgs, List[str]]

OptionalKeyPairCommandArgs = Optional[KeyPairCommandArgs]
OptionalCommandArgs = Optional[CommandArgs]

CoreStringCommand = str
StringsKeyPair = Dict[str, str]
