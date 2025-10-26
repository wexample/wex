from __future__ import annotations

from typing import TYPE_CHECKING

from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
    from src.utils.kernel import Kernel


@command(help="Return a queued collection")
def test__return_type__queued_collection(kernel: Kernel) -> QueuedCollectionResponse:
    from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse

    return QueuedCollectionResponse(kernel, ["lorem", "ipsum", 123])
