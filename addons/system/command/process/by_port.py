from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON, DATE_FORMAT_SECOND
from src.helper.system import get_processes_by_port
from src.core.response.DictResponse import DictResponse
from datetime import datetime


@command(help="Return process info", command_type=COMMAND_TYPE_ADDON)
@option('--port', '-p', type=int, required=True, help="Port number")
def system__process__by_port(kernel: Kernel, port: int):
    process = get_processes_by_port(port)
    output_list = DictResponse(kernel, 'Process')

    if process:
        output_list.set_dictionary({
            'Name': process.name(),
            'Port': port,
            'Pid': process.pid,
            'Status': process.status(),
            'Started': datetime.fromtimestamp(process.create_time()).strftime(DATE_FORMAT_SECOND),
        })

    else:
        output_list.set_dictionary({
            'Port': port,
            'Running': False
        })

    return output_list
