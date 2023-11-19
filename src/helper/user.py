from __future__ import annotations

import getpass
import grp
import os
import pwd
from typing import Optional

from addons.app.const.app import APP_DIR_APP_DATA


def get_sudo_username() -> str | None:
    return os.getenv('SUDO_USER')


def get_user_or_sudo_user() -> str:
    return get_sudo_username() or getpass.getuser()


def get_uid_from_user_name(user: str) -> int:
    return pwd.getpwnam(user).pw_uid


def get_gid_from_group_name(group: str) -> int:
    return grp.getgrnam(group).gr_gid


def get_user_group_name(user: str) -> str:
    user_info = pwd.getpwnam(user)
    # Get the group's entry using the user's gid
    group = grp.getgrgid(user_info.pw_gid)

    return group.gr_name


def get_sudo_gid() -> int | None:
    gid = os.getenv('SUDO_GID')
    return int(gid) if gid else None


def get_sudo_group() -> str | None:
    gid = get_sudo_gid()
    return grp.getgrgid(gid).gr_name if gid else None


def get_user_or_sudo_user_home_data_path() -> str:
    sudo_username = get_sudo_username()
    if sudo_username is None:
        return f"{os.path.expanduser('~')}/"
    else:
        return f'/home/{get_sudo_username()}/'


def set_owner_recursively(path: str, user: Optional[str] = None, group: Optional[str] = None) -> None:
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


def set_permissions_recursively(path: str, mode: int) -> None:
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


def get_user_home_data_path() -> str:
    return f"{os.path.expanduser('~')}/{APP_DIR_APP_DATA}"


def create_user_home_data_path() -> str:
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
    except Exception:
        return False
