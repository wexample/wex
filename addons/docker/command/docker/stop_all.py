from typing import TYPE_CHECKING, cast

from src.const.types import ShellCommandsDeepList
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Stop all running docker feature : containers, networks, volumes")
def docker__docker__stop_all(kernel: "Kernel") -> QueuedCollectionResponse:
    return QueuedCollectionResponse(
        kernel,
        [
            InteractiveShellCommandResponse(
                kernel,
                cast(
                    ShellCommandsDeepList,
                    [
                        "docker",
                        "stop",
                        [
                            "docker",
                            "ps",
                            "-qa",
                        ],
                    ],
                ),
                True,
            ),
            InteractiveShellCommandResponse(
                kernel,
                cast(
                    ShellCommandsDeepList,
                    [
                        "docker",
                        "rm",
                        [
                            "docker",
                            "ps",
                            "-qa",
                        ],
                    ],
                ),
                True,
            ),
            InteractiveShellCommandResponse(
                kernel,
                cast(
                    ShellCommandsDeepList,
                    [
                        "docker",
                        "network",
                        "rm",
                        ["docker", "network", "ls", "-q", "--filter", "type=custom"],
                    ],
                ),
                True,
            ),
            InteractiveShellCommandResponse(
                kernel,
                cast(
                    ShellCommandsDeepList,
                    ["docker", "volume", "rm", ["docker", "volume", "ls", "-q"]],
                ),
                True,
            ),
        ],
    )
