import os
import shutil
from typing import TYPE_CHECKING, Any, Dict, List, cast

from addons.app.const.app import APP_DIR_APP_DATA, APP_FILE_APP_SERVICE_CONFIG
from src.helper.data_yaml import yaml_load

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager
    from src.core.Kernel import Kernel


def service_get_dir(kernel: "Kernel", service: str) -> str | bool:
    dirs = service_get_all_dirs(kernel)

    # Service dir is missing,
    # it doesn't exist
    if service not in dirs:
        return False

    return dirs[service]


def service_load_config(kernel: "Kernel", service: str) -> Any:
    dirs = service_get_all_dirs(kernel)

    if service not in dirs:
        return False

    # Allow service to not define a config file
    return yaml_load(
        os.path.join(dirs[service], APP_FILE_APP_SERVICE_CONFIG)
    )


def service_get_inheritance_tree(kernel: "Kernel", service: str) -> List[str]:
    # Initialize an empty list to store the inheritance tree
    inheritance_tree: List[str] = []

    # Get the configuration of the given service
    service_config = service_load_config(kernel, service)

    if not service_config:
        return [service]

    # Check if the service has an 'extends' property
    parent_service = service_config.get("extends")

    # If it does, recursively find its inheritance tree
    if parent_service:
        inheritance_tree.extend(service_get_inheritance_tree(kernel, parent_service))

    # Add the current service to the inheritance tree
    inheritance_tree.append(service)

    # Reverse the list to make the original service the first element
    inheritance_tree.reverse()

    return inheritance_tree


def service_copy_sample_dir(kernel: "Kernel", service: str, subdir: str) -> None:
    service_dir = service_get_dir(kernel, service)
    if not isinstance(service_dir, str):
        return

    service_sample_dir_env = (
        os.path.join(service_dir, "samples", APP_DIR_APP_DATA) + os.sep
    )

    manager = cast("AppAddonManager", kernel.addons["app"])

    env_dir: str = f"{manager.app_dir}{APP_DIR_APP_DATA}"

    shutil.copytree(
        service_sample_dir_env + os.sep + subdir,
        env_dir + os.sep + subdir,
        dirs_exist_ok=True,
    )


def service_get_all_dirs(kernel: "Kernel") -> Dict[str, str]:
    dirs = {}

    for addon in kernel.addons:
        services_dir = kernel.get_path("addons", [addon, "services"])
        if os.path.exists(services_dir):
            for service in os.listdir(services_dir):
                dirs[service] = os.path.join(services_dir, service) + os.sep

    return dirs
