from src.decorator.command import command
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return a queued collection")
def test__return_type__queued_collection(kernel: 'Kernel'):
    return QueuedCollectionResponse(kernel, [
        'lorem',
        'ipsum',
        123
    ])
