import os
import grp
import signal
import socket
import subprocess
from contextlib import closing
import psutil

from addons.app.const.app import APP_DIR_APP_DATA
from src.helper.command import execute_command


def get_sudo_username():
    return os.getenv('SUDO_USER')


def get_sudo_gid():
    return int(os.getenv('SUDO_GID'))


def get_sudo_group():
    return grp.getgrgid(
        get_sudo_gid()
    ).gr_name


def get_user_or_sudo_user_home_data_path():
    sudo_username = get_sudo_username()
    if sudo_username is None:
        return f"{os.path.expanduser('~')}/"
    else:
        return f'/home/{get_sudo_username()}/'


def get_user_home_data_path():
    return f"{os.path.expanduser('~')}/{APP_DIR_APP_DATA}"


def create_user_home_data_path():
    path = f'{get_user_or_sudo_user_home_data_path()}{APP_DIR_APP_DATA}'

    os.makedirs(
        os.path.dirname(
            path
        ),
        exist_ok=True
    )

    return path


def is_port_open(port: int, host: str = 'localhost') -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False


def get_pid_from_port(port: int):
    for proc in psutil.process_iter(['pid', 'connections']):
        for conn in proc.info['connections']:
            if conn.laddr.port == port:
                return proc.info['pid']
    return None


def kill_process_by_port(port: int):
    pid = get_pid_from_port(port)

    if pid:
        os.kill(int(pid), signal.SIGTERM)


def kill_process_by_command(kernel, command: str):
    process = execute_command(
        kernel,
        [
            'pgrep',
            '-f',
            command
        ],
        # Sync mode.
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = process.communicate()

    for pid in out.splitlines():
        os.kill(int(pid), signal.SIGTERM)


def service_daemon_reload(kernel, command: str = 'daemon-reload'):
    execute_command(
        kernel,
        ['systemctl', command]
    )


def service_exec(kernel, service, action: str):
    execute_command(
        kernel,
        [
            'systemctl',
            action,
            service
        ]
    )
