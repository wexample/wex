from __future__ import annotations

import os
import socket
from contextlib import closing
from src.core import Kernel
from src.helper.command import execute_command


def system_is_port_open(port: int, host: str = 'localhost') -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False


def system_service_daemon_reload(kernel: Kernel, command: str = 'daemon-reload') -> None:
    execute_command(
        kernel,
        ['systemctl', command]
    )


def system_service_exec(kernel: Kernel, service: str, action: str) -> None:
    execute_command(
        kernel,
        [
            'systemctl',
            action,
            service
        ]
    )


def system_get_bashrc_handler_path(kernel: Kernel) -> str:
    return os.path.join(kernel.get_path('root'), 'cli', "bashrc-handler")


def system_get_daemon_service_path(kernel: Kernel) -> str:
    return f'. {system_get_bashrc_handler_path(kernel)}'
