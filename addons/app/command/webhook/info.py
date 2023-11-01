from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON, WEBHOOK_LISTEN_PORT_DEFAULT, KERNEL_RENDER_MODE_NONE
from addons.system.command.process.by_port import system__process__by_port
from src.decorator.command import command
from src.decorator.as_sudo import as_sudo
from addons.app.command.webhook.exec import app__webhook__exec


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
@as_sudo
def app__webhook__info(kernel: Kernel):
    response = kernel.run_function(
        system__process__by_port,
        {
            'port': WEBHOOK_LISTEN_PORT_DEFAULT
        },
        render_mode=KERNEL_RENDER_MODE_NONE
    )

    response.new_section('Log')

    logs = kernel.logger.find_by_function(
        app__webhook__exec
    )

    output = []

    for log in logs:
        output.append(
            kernel.logger.build_summary(
                log
            )
        )

    response.set_body(output)

    return response

