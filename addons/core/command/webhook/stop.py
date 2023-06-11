import click

from addons.core.command.webhook.serve import core__webhook__serve
from addons.system.command.system.is_docker import system__system__is_docker
from helper.file import remove_file_if_exists
from src.const.globals import SERVICE_DAEMON_NAME, SERVICE_DAEMON_PATH
from src.helper.system import kill_process_by_command, service_exec, service_daemon_reload
from src.helper.command import build_command_from_function
from src.decorator.as_sudo import as_sudo


@click.command()
@click.pass_obj
@as_sudo
def core__webhook__stop(
        kernel,
):
    use_daemon = not kernel.exec_function(system__system__is_docker)

    if use_daemon:
        service_exec(kernel, SERVICE_DAEMON_NAME, 'stop')
        service_exec(kernel, SERVICE_DAEMON_NAME, 'disable')
        remove_file_if_exists(SERVICE_DAEMON_PATH)
        service_daemon_reload(kernel)
        service_daemon_reload(kernel, 'reset-failed')
    else:
        kill_process_by_command(
            kernel,
            build_command_from_function(
                core__webhook__serve
            )
        )

    kernel.message(f'Webhook server stopped')
