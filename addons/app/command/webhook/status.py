import re

from addons.app.decorator.option_webhook_listener import option_webhook_listener
from src.helper.args import arg_shift
from src.core.response.DictResponse import DictResponse
from src.core.response.TableResponse import TableResponse
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON, WEBHOOK_LISTEN_PORT_DEFAULT, KERNEL_RENDER_MODE_NONE, \
    KERNEL_RENDER_MODE_TERMINAL
from addons.system.command.process.by_port import system__process__by_port
from src.decorator.command import command
from src.decorator.as_sudo import as_sudo
from addons.app.command.webhook.exec import app__webhook__exec


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option_webhook_listener(port=True)
@as_sudo()
def app__webhook__status(kernel: Kernel, port: None | int = None):
    from addons.app.command.webhook.listen import WEBHOOK_LISTENER_ROUTES_MAP

    port = port or WEBHOOK_LISTEN_PORT_DEFAULT

    response = kernel.run_function(
        system__process__by_port,
        {
            'port': port
        },
        render_mode=KERNEL_RENDER_MODE_NONE
    )

    # Hide sensitive info
    if 'command' in response.dictionary_data:
        del response.dictionary_data['command']

    logs = kernel.logger.find_by_function(
        app__webhook__exec
    )

    table = []
    for log in logs:
        if len(log['commands']):
            command_data_first = log['commands'][0]
            path = arg_shift(command_data_first['args'], 'path')

            match = re.match(
                WEBHOOK_LISTENER_ROUTES_MAP['exec']['pattern'],
                path
            )

            table.append(
                [
                    log['dateStart'],
                    match[1],
                    match[2],
                    log['status']
                ]
            )

    table_response = TableResponse(kernel)
    table_response.set_title('Log')
    table_response.set_body(table)

    return DictResponse(kernel, {
        "process": response,
        "log": table_response,
    }, cli_render_mode=KERNEL_RENDER_MODE_TERMINAL)
