import os
import shutil

from addons.app.const.app import APP_DIR_APP_DATA, APP_FILE_APP_SERVICE_CONFIG
from src.helper.json import load_json_if_valid


def get_service_dir(kernel, service: str) -> str | bool:
    dirs = service_get_all_dirs(kernel)

    # Service dir is missing,
    # it doesn't exist
    if service not in dirs:
        return False

    return dirs[service]


def service_load_config(kernel, service) -> dict | bool:
    dirs = service_get_all_dirs(kernel)

    # Allow service to not define a config file
    return load_json_if_valid(
        os.path.join(dirs[service], APP_FILE_APP_SERVICE_CONFIG)
    ) or {}


def service_get_inheritance_tree(kernel, service):
    # Initialize an empty list to store the inheritance tree
    inheritance_tree = []

    # Get the configuration of the given service
    service_config = service_load_config(kernel, service)

    # Check if the service has an 'extends' property
    parent_service = service_config.get('extends')

    # If it does, recursively find its inheritance tree
    if parent_service:
        inheritance_tree.extend(service_get_inheritance_tree(kernel, parent_service))

    # Add the current service to the inheritance tree
    inheritance_tree.append(service)

    # Reverse the list to make the original service the first element
    inheritance_tree.reverse()

    return inheritance_tree


def copy_service_sample_dir(kernel, service: str, subdir: str):
    service_dir = get_service_dir(kernel, service)
    service_sample_dir = os.path.join(service_dir, 'samples') + '/'
    service_sample_dir_env = os.path.join(service_sample_dir, APP_DIR_APP_DATA) + '/'

    from addons.app.AppAddonManager import AppAddonManager
    manager: AppAddonManager = kernel.addons['app']
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'

    shutil.copytree(service_sample_dir_env + '/' + subdir, env_dir + '/' + subdir, dirs_exist_ok=True)


def service_get_all_dirs(kernel) -> dict:
    dirs = {}

    for addon in kernel.addons:
        services_dir = kernel.get_path('addons', [addon, 'services'])
        if os.path.exists(services_dir):
            for service in os.listdir(services_dir):
                dirs[service] = os.path.join(services_dir, service) + os.sep

    return dirs
