from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON, WEBHOOK_LISTEN_PORT_DEFAULT
from addons.system.command.process.by_port import system__process__by_port
from src.decorator.command import command


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def app__webhook__info(kernel: Kernel):
    return kernel.run_function(
        system__process__by_port,
        {
            'port': WEBHOOK_LISTEN_PORT_DEFAULT
        }
    )
