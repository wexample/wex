from typing import TYPE_CHECKING

from addons.test.command.return_type.function import _test__return_type__function
from src.core.response.DefaultResponse import DefaultResponse
from src.core.response.DictResponse import DictResponse
from src.core.response.FunctionResponse import FunctionResponse
from src.core.response.HiddenResponse import HiddenResponse
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.core.response.KeyValueResponse import KeyValueResponse
from src.core.response.NonInteractiveShellCommandResponse import (
    NonInteractiveShellCommandResponse,
)
from src.core.response.NullResponse import NullResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.core.response.TableResponse import TableResponse
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return a string")
def test__return_type__response_collection(kernel: "Kernel"):
    return ResponseCollectionResponse(
        kernel,
        [
            DefaultResponse(kernel, "DEFAULT"),
            DictResponse(kernel, {"lorem": "ipsum"}),
            FunctionResponse(kernel, _test__return_type__function),
            HiddenResponse(kernel, "HIDDEN_RESPONSE"),
            InteractiveShellCommandResponse(
                kernel, ["echo", "INTERACTIVE_SHELL_COMMAND_RESPONSE"]
            ),
            KeyValueResponse(kernel, {"key": "value"}),
            NonInteractiveShellCommandResponse(
                kernel, ["echo", "NON_INTERACTIVE_SHELL_COMMAND_RESPONSE"]
            ),
            NullResponse(kernel),
            # Not supported yet QueuedCollectionResponse()
            # Not supported yet ResponseCollectionResponse()
            TableResponse(kernel, "Test Table", [["lorem", "ipsum"], ["dolor", "sit"]]),
        ],
    )
