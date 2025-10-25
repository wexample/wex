from __future__ import annotations

from typing import TYPE_CHECKING, cast
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel
    from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse


@command(help="Stop all running docker feature : containers, networks, volumes")
def docker__docker__stop_all(kernel: Kernel) -> QueuedCollectionResponse:
    from src.core.response.InteractiveShellCommandResponse import (
        InteractiveShellCommandResponse,
    )
    from src.const.types import ShellCommandsDeepList
    from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse

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
