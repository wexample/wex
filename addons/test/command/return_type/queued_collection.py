from src.decorator.command import command
from src.core import Kernel
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse


@command(help="Return a queued collection")
def test__return_type__queued_collection(kernel: Kernel):
    return QueuedCollectionResponse(kernel, [
        'lorem',
        'ipsum',
        123
    ])
