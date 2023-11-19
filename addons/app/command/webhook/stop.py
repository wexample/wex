
from addons.app.command.webhook.listen import app__webhook__listen
from addons.system.command.system.is_docker import system__system__is_docker
from src.helper.file import file_remove_file_if_exists
from src.const.globals import SERVICE_DAEMON_NAME, SERVICE_DAEMON_PATH, COMMAND_TYPE_ADDON
from src.helper.system import service_exec, service_daemon_reload
from src.helper.process import process_kill_by_command
from src.decorator.as_sudo import as_sudo
from src.core.Kernel import Kernel
from src.decorator.command import command


@as_sudo()
@command(help="Stop webhook daemon")
def app__webhook__stop(
        kernel: Kernel,
):
    use_daemon = not kernel.run_function(system__system__is_docker).first()

    if use_daemon:
        service_exec(kernel, SERVICE_DAEMON_NAME, 'stop')
        service_exec(kernel, SERVICE_DAEMON_NAME, 'disable')
        file_remove_file_if_exists(SERVICE_DAEMON_PATH)
        service_daemon_reload(kernel)
        service_daemon_reload(kernel, 'reset-failed')

        kernel.io.message(f'Webhook server daemon stopped')
    else:
        process_kill_by_command(
            kernel,
            kernel.get_command_resolver(COMMAND_TYPE_ADDON).build_full_command_from_function(
                app__webhook__listen
            )
        )

        kernel.io.message(f'Webhook server process killed')
