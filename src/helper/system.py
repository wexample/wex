from __future__ import annotations

import os
import grp
import pwd
import signal
import socket
from contextlib import closing
from typing import Optional
import psutil
import getpass

from addons.app.const.app import APP_DIR_APP_DATA
from src.core import Kernel
from src.helper.command import execute_command


def get_processes_by_port(port: int) -> Optional[psutil.Process]:
    port = int(port)

    for process in psutil.process_iter():
        try:
            connections = process.connections()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
        for connection in connections:
            if connection.laddr.port == port:
                return process
    return None


def get_sudo_username():
    return os.getenv('SUDO_USER')


def get_user_or_sudo_user() -> str:
    sudo_username = get_sudo_username()

    if sudo_username is None:
        return getpass.getuser()
    else:
        return get_sudo_username()


def get_uid_from_user_name(user: str) -> int:
    return pwd.getpwnam(user).pw_uid


def get_gid_from_group_name(group: str) -> int:
    return grp.getgrnam(group).gr_gid


def get_user_group_name(user: str):
    user_info = pwd.getpwnam(user)
    # Get the group's entry using the user's gid
    group = grp.getgrgid(user_info.pw_gid)

    return group.gr_name


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


def set_home_path_permissions():
    os.chown(
        f'{get_user_or_sudo_user_home_data_path()}{APP_DIR_APP_DATA}'
    )


def set_owner_recursively(path: str, user: str = None, group: str = None):
    if user is None:
        user = get_user_or_sudo_user()

    if group is None:
        group = get_user_group_name(user)

    uid = get_uid_from_user_name(user)
    gid = get_gid_from_group_name(group)

    # Change owner for the current path
    try:
        if os.path.islink(path):
            os.lchown(path, uid, gid)  # Change owner of the symlink itself
        else:
            os.chown(path, uid, gid)  # Change owner of the file/directory
    except FileNotFoundError:
        pass

    # If the path is a directory, loop through its contents and call the function recursively
    if os.path.isdir(path) and not os.path.islink(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            set_owner_recursively(item_path, user, group)


def set_permissions_recursively(path: str, mode: int):
    # Change permissions for the current path

    try:
        if not os.path.islink(path):
            os.chmod(path, mode)  # Change owner of the file/directory
    except FileNotFoundError:
        pass

    # If the path is a directory, loop through its contents and call the function recursively
    if os.path.isdir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            set_permissions_recursively(item_path, mode)


def is_current_user_sudo() -> bool:
    return os.getuid() == 0


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


def user_exists(username: str) -> bool:
    try:
        # Attempt to get user details
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def is_port_open(port: int, host: str = 'localhost') -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False


def kill_process(process: Optional[psutil.Process]):
    if process is None:
        return False
    try:
        process.terminate()
        return True
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return False


def kill_process_by_port(port: int):
    kill_process(
        get_processes_by_port(
            port
        )
    )


def kill_process_by_command(kernel, command: str):
    success, pids = execute_command(
        kernel,
        [
            'pgrep',
            '-f',
            command
        ]
    )

    if pids:
        for pid in pids:
            kernel.io.log(f'Killing process {pid}')
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


def is_sudo(username: str) -> bool:
    try:
        with open("/etc/sudoers", "r") as f:
            content = f.readlines()

        for line in content:
            if line.strip().startswith(username):
                return True

        import os
        for file in os.listdir("/etc/sudoers.d/"):
            with open(os.path.join("/etc/sudoers.d/", file), "r") as f:
                content = f.readlines()
            for line in content:
                if line.strip().startswith(username):
                    return True

        return False
    except Exception as e:
        return False


def system_get_bashrc_handler_path(kernel: Kernel) -> str:
    return os.path.join(kernel.get_path('root'), 'cli', "bashrc-handler")


def system_get_daemon_service_path(kernel: Kernel) -> str:
    return f'. {system_get_bashrc_handler_path(kernel)}'
