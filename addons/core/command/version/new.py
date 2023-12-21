from typing import TYPE_CHECKING

from git import Repo  # type: ignore

from addons.core.command.version.new_commit import core__version__new_commit
from addons.core.command.version.new_write import core__version__new_write
from addons.default.const.default import UPGRADE_TYPE_MINOR
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Build a new version of current core, or commit new version changes")
@option("--type", "-t", type=str, required=False, help="Type of update")
def core__version__new(
    kernel: "Kernel", type: str = UPGRADE_TYPE_MINOR
) -> QueuedCollectionResponse:
    def _write(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        return kernel.run_function(
            core__version__new_write,
            {
                "type": type,
            },
        )

    def _commit(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        return kernel.run_function(core__version__new_commit)

    return QueuedCollectionResponse(
        kernel,
        [_write, _commit],
    )
