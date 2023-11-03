
from addons.app.command.webhook.listen import app__webhook__listen
from addons.system.command.system.is_docker import system__system__is_docker
from src.helper.file import remove_file_if_exists
from src.const.globals import SERVICE_DAEMON_NAME, SERVICE_DAEMON_PATH, COMMAND_TYPE_ADDON
from src.helper.system import kill_process_by_command, service_exec, service_daemon_reload
from src.decorator.as_sudo import as_sudo
from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Stop webhook daemon")
@as_sudo()
def app__webhook__stop(
        kernel: Kernel,
):
    use_daemon = not kernel.run_function(system__system__is_docker)

    if use_daemon:
        service_exec(kernel, SERVICE_DAEMON_NAME, 'stop')
        service_exec(kernel, SERVICE_DAEMON_NAME, 'disable')
        remove_file_if_exists(SERVICE_DAEMON_PATH)
        service_daemon_reload(kernel)
        service_daemon_reload(kernel, 'reset-failed')
    else:
        kill_process_by_command(
            kernel,
            kernel.get_command_resolver(COMMAND_TYPE_ADDON).build_full_command_from_function(
                app__webhook__listen
            )
        )

    kernel.io.message(f'Webhook server stopped')
