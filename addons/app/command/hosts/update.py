import os.path
from typing import TYPE_CHECKING, Optional

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.started import app__app__started
from addons.docker.command.docker.ip import docker__docker__ip
from src.const.globals import CORE_COMMAND_NAME, SYSTEM_HOSTS_PATH
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Update local /etc/hosts file")
@option("--env", "-e", type=str, required=False, help="Env for accessing apps")
def app__hosts__update(kernel: "Kernel", env: Optional[str] = None) -> None:
    new_block_content_list = []
    ip = kernel.run_function(docker__docker__ip).first()

    manager: AppAddonManager = AppAddonManager(kernel)
    for app_name, app_dir in manager.get_proxy_apps(env).items():
        # Filter out missing folders
        if os.path.exists(app_dir):
            manager.set_app_workdir(app_dir)

            if kernel.run_function(app__app__started, {"app-dir": app_dir}).first():
                kernel.io.log(f"Found app [{app_name}]")

                if manager.has_runtime_config("domains"):
                    domains = manager.get_runtime_config("domains").get_list()

                    for domain in domains:
                        new_block_content_list.append(f"{ip}\t{domain}")

    new_block_content = os.linesep.join(new_block_content_list)

    kernel.io.log(f"Updating {SYSTEM_HOSTS_PATH}")

    with open(SYSTEM_HOSTS_PATH, "r") as f:
        hosts_content = f.read()

    # Remove old wex block
    hosts_content = remove_domains_block(hosts_content)
    # Add the new wex block
    hosts_content = add_domains_block(hosts_content, new_block_content)

    # Write the updated content back to the file
    with open(SYSTEM_HOSTS_PATH, "w") as f:
        f.write(hosts_content)


def remove_domains_block(text: str) -> str:
    """
    Removes any text surrounded by "#[ wex ]#...#[ end-wex ]#" in a given string variable.
    """
    lines = text.split(os.linesep)
    new_lines = []
    in_wex_block = False

    for line in lines:
        if f"#[ {CORE_COMMAND_NAME} ]#" in line:
            in_wex_block = True
        elif f"#[ end-{CORE_COMMAND_NAME} ]#" in line:
            in_wex_block = False
            continue

        if not in_wex_block:
            new_lines.append(line)

    return os.linesep.join(new_lines)


def add_domains_block(text: str, block_content: str) -> str:
    """
    Adds a text surrounded by "#[ wex ]#...#[ end-wex ]#" in a given string variable.
    """
    return (
        text
        + f"#[ {CORE_COMMAND_NAME} ]#{os.linesep}{block_content}{os.linesep}#[ end-{CORE_COMMAND_NAME} ]#{os.linesep}"
    )
