import os
import grp
import signal
import socket
import subprocess
from contextlib import closing
import psutil

from helper.command import execute_command


def get_sudo_username():
    return os.getenv('SUDO_USER')


def get_sudo_gid():
    return int(os.getenv('SUDO_GID'))


def get_sudo_group():
    return grp.getgrgid(
        get_sudo_gid()
    ).gr_name


def get_sudo_user_home_path():
    return f'/home/{get_sudo_username()}/'


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
