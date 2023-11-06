from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse


@command(help="Count with a queue to check arguments passing", command_type=COMMAND_TYPE_ADDON)
@option('--initial', '-i', type=int, required=True, help="Argument")
def test__demo_command__counting_collection(kernel: Kernel, initial: int):
    def callback(previous):
        kernel.io.log('INITIAL ' + str(initial))
        kernel.io.log('PREVIOUS ' + str(previous))
        return previous + 1

    return QueuedCollectionResponse(kernel, [
        initial,
        callback,
        callback,
        callback,
        callback,
    ])
