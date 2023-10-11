import os
import glob

from addons.app.const.app import APP_DIR_APP_DATA
from addons.default.helpers.git import file_move_or_git_move, get_or_create_repo
from addons.default.helpers.migration import migration_delete_dir_if_empty
from addons.app.helpers.app import create_env
from src.helper.prompt import progress_steps
from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager


def migration_4_0_0(kernel: Kernel, manager: AppAddonManager):
    repo = get_or_create_repo(manager.app_dir)
    projects_dirs = ['project', 'wordpress']

    # Rename ".wex" file to "config"
    def _migration_4_0_0_config():
        if os.path.isfile('.wex'):
            # Rename old config file
            file_move_or_git_move(repo, '.wex', 'config')

    # Create ".wex" dir
    def _migration_4_0_0_dir():
        new_dir_path = f"{manager.app_dir}/.wex"
        # Make the directory
        os.makedirs(new_dir_path, exist_ok=True)
        os.makedirs(new_dir_path + '/tmp', exist_ok=True)

    # Move every file and folder to ".wex", except the "project" dir
    def _migration_4_0_0_move_root_environment_files():
        for item in os.listdir(manager.app_dir):
            if item in projects_dirs + ['.git', '.wex']:
                continue
            file_move_or_git_move(repo, item, f'.wex/{item}')

        if not os.path.exists('.wex/.env'):
            create_env('prod', manager.app_dir)

    # Move every file and folder from project/* to root (app_dir)
    def _migration_4_0_0_move_project_files():
        for projects_dir in projects_dirs:
            dir_project = os.path.join(manager.app_dir, projects_dir)

            if os.path.exists(dir_project):
                for item in os.listdir(dir_project):
                    file_move_or_git_move(repo, f'{projects_dir}/{item}', item)

            migration_delete_dir_if_empty(kernel, dir_project)

    def _migration_4_0_0_update_docker():
        _migration_4_0_0_replace_docker_placeholders(manager, {
            'SITE_NAME': 'APP_NAME',
        })

    progress_steps(kernel, [
        _migration_4_0_0_config,
        _migration_4_0_0_dir,
        _migration_4_0_0_move_root_environment_files,
        _migration_4_0_0_move_project_files,
        _migration_4_0_0_update_docker,
    ])


def _migration_4_0_0_et_docker_files(manager: AppAddonManager):
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'

    # Convert docker files.
    docker_dir = f'{env_dir}docker/'

    return glob.glob(f"{docker_dir}docker-compose.*")


def _migration_4_0_0_replace_docker_placeholders(manager: AppAddonManager, replacement_mapping: dict):
    docker_files = _migration_4_0_0_et_docker_files(manager)

    # Raw file replacements
    # Loop through each docker-compose file
    for docker_file in docker_files:
        # Read the file content
        with open(docker_file, 'r') as f:
            content = f.read()

        # Replace strings based on the mapping dictionary
        for old_str, new_str in replacement_mapping.items():
            content = content.replace('${' + str(old_str) + '}', '${' + str(new_str) + '}')

        # Override the file with updated content
        with open(docker_file, 'w') as f:
            f.write(content)


def is_version_4_0_0(kernel: Kernel, path: str):
    if os.path.isdir(path + '.wex'):
        if os.path.isfile(path + '.wex/config'):
            return True

    return None
