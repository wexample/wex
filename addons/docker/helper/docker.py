import grp
import pwd
import yaml

from src.helper.command import execute_command_sync
from src.helper.dict import dict_merge
from src.helper.user import is_sudo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def user_has_docker_permission(username: str) -> bool:
    if is_sudo(username):
        return True

    try:
        user_groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
        gid = pwd.getpwnam(username).pw_gid
        user_groups.append(grp.getgrgid(gid).gr_name)

        return "docker" in user_groups
    except KeyError:
        return False


def merge_docker_compose_files(src: str, target: str) -> None:
    # Load both files as Python objects
    with open(src, "r") as f:
        data1 = yaml.safe_load(f)
    with open(target, "r") as f:
        data2 = yaml.safe_load(f) or {}

    # Recursively merge the two objects
    merged_data = dict_merge(data1, data2)

    # Write the merged data to a new file
    with open(target, "w") as f:
        yaml.dump(merged_data, f)


def docker_container_ip(kernel: "Kernel", container_name: str) -> str:
    success, diff = execute_command_sync(
        kernel,
        [
            "docker",
            "inspect",
            "-f",
            "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
            container_name
        ]
    )

    return diff[0]
