import os

from addons.default.helpers.git import file_move_or_git_move, get_or_create_repo
from addons.default.helpers.migration import migration_delete_dir_if_empty
from src.helper.prompt import progress_steps
from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager


def migration_4_0_0(kernel: Kernel, manager: AppAddonManager):
    repo = get_or_create_repo(manager.app_dir)

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
            if item in ["project", ".git", ".wex"]:
                continue
            file_move_or_git_move(repo, item, f'.wex/{item}')

    # Move every file and folder from project/* to root (app_dir)
    def _migration_4_0_0_move_project_files():
        dir_project = os.path.join(manager.app_dir, "project")

        if os.path.exists(dir_project):
            for item in os.listdir(dir_project):
                file_move_or_git_move(repo, f'project/{item}', item)

        migration_delete_dir_if_empty(kernel, dir_project)

    progress_steps(kernel, [
        _migration_4_0_0_config,
        _migration_4_0_0_dir,
        _migration_4_0_0_move_root_environment_files,
        _migration_4_0_0_move_project_files,
    ])


def is_version_4_0_0(kernel: Kernel, path: str):
    if os.path.isdir(path + '.wex'):
        if os.path.isfile(path + '.wex/config'):
            return True

    return None
