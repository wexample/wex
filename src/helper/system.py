from __future__ import annotations

import os
import socket
from contextlib import closing
from typing import TYPE_CHECKING

from src.const.globals import SERVICE_DAEMON_NAME
from src.const.types import Kwargs
from src.helper.command import execute_command_sync
from src.helper.process import process_get_all_by_port

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def system_is_port_open(port: int, host: str = "localhost") -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False


def system_port_check(kernel: "Kernel", port_to_check: int) -> None:
    if not port_to_check:
        kernel.io.error(f"Invalid port {port_to_check}", trace=False)

    kernel.io.log(f"Checking that port {port_to_check} is free")

    # Check port availability.
    process = process_get_all_by_port(port_to_check)
    if process:
        kernel.io.error(
            f"Process {process.pid} ({process.name()}) is using port {port_to_check}",
            trace=False,
        )

    kernel.io.success(f"Port {port_to_check} free")


def system_service_daemon_reload(
    kernel: "Kernel", command: str = "daemon-reload"
) -> None:
    execute_command_sync(kernel, ["systemctl", command], as_sudo_user=False)


def system_service_daemon_exec(kernel: "Kernel", action: str) -> None:
    system_service_exec(kernel, SERVICE_DAEMON_NAME, action, ignore_error=True)


def system_service_exec(
    kernel: "Kernel", service: str, action: str, **kwargs: Kwargs
) -> None:
    execute_command_sync(
        kernel, ["systemctl", action, service], **kwargs, as_sudo_user=False
    )


def system_get_bashrc_handler_path(kernel: "Kernel") -> str:
    return os.path.join(kernel.directory.path, "cli", "bashrc-handler")


def system_get_daemon_service_path(kernel: "Kernel") -> str:
    return f". {system_get_bashrc_handler_path(kernel)}"
