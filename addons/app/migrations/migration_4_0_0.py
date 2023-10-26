import os
import glob

from addons.app.const.app import APP_DIR_APP_DATA, APP_ENV_LOCAL
from addons.default.helpers.git import file_move_or_git_move, get_or_create_repo
from addons.default.helpers.migration import migration_delete_dir_if_empty
from addons.app.helpers.app import create_env
from src.helper.prompt import progress_steps
from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager


def migration_4_0_0(kernel: Kernel, manager: AppAddonManager):
    repo = get_or_create_repo(manager.app_dir)
    projects_dirs = ['project', 'wordpress']

    def _migration_4_0_0_env():
        _migration_4_0_0_replace_placeholders(
            manager.app_dir + '.env',
            {
                'SITE_ENV': 'APP_ENV',
            }
        )

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

    # Move every file and folder to ".wex", except the "project" dir
    def _migration_4_0_0_move_root_environment_files():
        for item in os.listdir(manager.app_dir):
            if item in projects_dirs + ['.git', '.wex']:
                continue
            file_move_or_git_move(repo, item, f'.wex/{item}')

        if not os.path.exists('.wex/.env'):
            create_env(APP_ENV_LOCAL, manager.app_dir)

        # May be missing.
        os.makedirs(f'.wex/tmp', exist_ok=True)

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
            'SITE_ENV': 'APP_ENV',
            'SITE_NAME': 'APP_NAME',
            'SITE_PATH_ROOT': 'APP_PATH_ROOT'
        })

    progress_steps(kernel, [
        _migration_4_0_0_env,
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


def _migration_4_0_0_replace_placeholders(file_path: str, replacement_mapping: dict):
    if not os.path.exists(file_path):
        return

    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()

    # Replace strings based on the mapping dictionary
    for old_str, new_str in replacement_mapping.items():
        content = content.replace(str(old_str), str(new_str))

    # Override the file with updated content
    with open(file_path, 'w') as f:
        f.write(content)


def _migration_4_0_0_replace_docker_placeholders(manager: AppAddonManager, replacement_mapping: dict):
    docker_files = _migration_4_0_0_et_docker_files(manager)
    converted_mapping = {}

    for old_str, new_str in replacement_mapping.items():
        converted_mapping['${' + str(old_str) + '}'] = '${' + str(new_str) + '}'

    # Raw file replacements
    # Loop through each docker-compose file
    for docker_file in docker_files:
        _migration_4_0_0_replace_placeholders(
            docker_file,
            converted_mapping
        )


def is_version_4_0_0(kernel: Kernel, path: str):
    if os.path.isdir(path + '.wex'):
        if os.path.isfile(path + '.wex/config'):
            return True

    return None
