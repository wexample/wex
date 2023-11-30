from typing import TYPE_CHECKING

from addons.app.command.webhook.listen import app__webhook__listen
from addons.system.command.system.is_docker import system__system__is_docker
from src.const.globals import COMMAND_TYPE_ADDON, SERVICE_DAEMON_PATH
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.helper.file import file_remove_file_if_exists
from src.helper.process import process_kill_by_command
from src.helper.system import system_service_daemon_exec, system_service_daemon_reload

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Stop webhook daemon")
def app__webhook__stop(
    kernel: "Kernel",
) -> None:
    use_daemon = not kernel.run_function(system__system__is_docker).first()

    if use_daemon:
        system_service_daemon_exec(kernel, "stop")
        system_service_daemon_exec(kernel, "disable")
        file_remove_file_if_exists(SERVICE_DAEMON_PATH)
        system_service_daemon_reload(kernel)
        system_service_daemon_reload(kernel, "reset-failed")

        kernel.io.message(f"Webhook server daemon stopped")
    else:
        process_kill_by_command(
            kernel,
            kernel.get_command_resolver(
                COMMAND_TYPE_ADDON
            ).build_full_command_from_function(app__webhook__listen),
        )

        kernel.io.message(f"Webhook server process killed")
