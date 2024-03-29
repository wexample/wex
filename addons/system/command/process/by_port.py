from datetime import datetime
from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON, DATE_FORMAT_SECOND
from src.core.response.KeyValueResponse import KeyValueResponse
from src.decorator.command import command
from src.decorator.option import option
from src.helper.process import process_get_all_by_port

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return process info", command_type=COMMAND_TYPE_ADDON)
@option("--port", "-p", type=int, required=True, help="Port number")
def system__process__by_port(kernel: "Kernel", port: int) -> KeyValueResponse:
    process = process_get_all_by_port(port)

    if process:
        dictionary = {
            "name": process.name(),
            "port": port,
            "pid": process.pid,
            "status": process.status(),
            "started": datetime.fromtimestamp(process.create_time()).strftime(
                DATE_FORMAT_SECOND
            ),
            "command": process.cmdline(),
            "running": True,
        }
    else:
        dictionary = {"port": port, "running": False}

    return KeyValueResponse(kernel, title="process", dictionary=dictionary)
