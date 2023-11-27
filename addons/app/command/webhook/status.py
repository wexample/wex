from typing import TYPE_CHECKING

from addons.app.decorator.option_webhook_listener import \
    option_webhook_listener
from addons.system.command.process.by_port import system__process__by_port
from src.const.globals import (COMMAND_TYPE_ADDON, KERNEL_RENDER_MODE_NONE,
                               KERNEL_RENDER_MODE_TERMINAL,
                               WEBHOOK_LISTEN_PORT_DEFAULT)
from src.core.response.DictResponse import DictResponse
from src.core.response.TableResponse import TableResponse
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Give information about webhook listener status", command_type=COMMAND_TYPE_ADDON)
@option_webhook_listener(port=True)
def app__webhook__status(kernel: 'Kernel', port: int = WEBHOOK_LISTEN_PORT_DEFAULT):
    response = kernel.run_function(
        system__process__by_port,
        {
            'port': port
        },
        render_mode=KERNEL_RENDER_MODE_NONE
    )

    output = {"process": response}

    if response.dictionary_data['running']:
        # Args are [python, main.py, task_id, ...]
        task_id = response.dictionary_data['command'][2]

        # Hide sensitive info
        if 'command' in response.dictionary_data:
            del response.dictionary_data['command']

        table = []

        listener_log = kernel.logger.load_logs(task_id)
        if listener_log:
            for children_time in listener_log['children']:
                children_id = listener_log['children'][children_time]

                children_log = kernel.logger.load_logs(children_id)

                table.append(
                    [
                        children_id,
                        children_log['command']['command'],
                        children_time,
                        children_log['status'],
                    ]
                )

        table_response = TableResponse(kernel)
        table_response.set_title('Log')
        table_response.set_body(table)

        output["log"] = table_response

    return DictResponse(kernel, output, cli_render_mode=KERNEL_RENDER_MODE_TERMINAL)
