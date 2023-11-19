from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON, DATE_FORMAT_SECOND
from src.helper.process import process_get_all_by_port
from src.core.response.KeyValueResponse import KeyValueResponse
from datetime import datetime


@command(help="Return process info", command_type=COMMAND_TYPE_ADDON)
@option('--port', '-p', type=int, required=True, help="Port number")
def system__process__by_port(kernel: Kernel, port: int):
    process = process_get_all_by_port(port)
    output_list = KeyValueResponse(kernel, title='process')

    if process:
        output_list.set_dictionary({
            'name': process.name(),
            'port': port,
            'pid': process.pid,
            'status': process.status(),
            'started': datetime.fromtimestamp(process.create_time()).strftime(DATE_FORMAT_SECOND),
            'command': process.cmdline(),
            'running': True
        })

    else:
        output_list.set_dictionary({
            'port': port,
            'running': False
        })

    return output_list
