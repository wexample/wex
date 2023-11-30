import glob
import os
from typing import TYPE_CHECKING, Optional

from addons.app.AppAddonManager import AppAddonManager
from addons.app.const.app import APP_DIR_APP_DATA, APP_ENV_LOCAL
from addons.app.helper.app import app_create_env
from addons.default.helper.git_utils import (
    git_get_or_create_repo,
    git_move_or_file_move,
)
from addons.default.helper.migration import migration_delete_dir_if_empty
from src.helper.prompt import prompt_progress_steps

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def migration_4_0_0(kernel: "Kernel", manager: AppAddonManager) -> None:
    repo = git_get_or_create_repo(manager.app_dir)
    projects_dirs = ["project", "wordpress"]

    def _migration_4_0_0_env() -> None:
        _migration_4_0_0_replace_placeholders(
            manager.app_dir + ".env",
            {
                "SITE_ENV": "APP_ENV",
            },
        )

    # Rename ".wex" file to "config"
    def _migration_4_0_0_config() -> None:
        if os.path.isfile(".wex"):
            # Rename old config file
            git_move_or_file_move(repo, ".wex", "config")

    # Create ".wex" dir
    def _migration_4_0_0_dir() -> None:
        new_dir_path = f"{manager.app_dir}/.wex"
        # Make the directory
        os.makedirs(new_dir_path, exist_ok=True)

    # Move every file and folder to ".wex", except the "project" dir
    def _migration_4_0_0_move_root_environment_files() -> None:
        for item in os.listdir(manager.app_dir):
            if item in projects_dirs + [".git", ".wex"]:
                continue
            git_move_or_file_move(repo, item, f".wex/{item}")

        if not os.path.exists(".wex/.env"):
            app_create_env(APP_ENV_LOCAL, manager.app_dir)

        # May be missing.
        os.makedirs(f".wex/tmp", exist_ok=True)

    # Move every file and folder from project/* to root (app_dir)
    def _migration_4_0_0_move_project_files() -> None:
        for projects_dir in projects_dirs:
            dir_project = os.path.join(manager.app_dir, projects_dir)

            if os.path.exists(dir_project):
                for item in os.listdir(dir_project):
                    git_move_or_file_move(repo, f"{projects_dir}/{item}", item)

            migration_delete_dir_if_empty(kernel, dir_project)

    def _migration_4_0_0_update_docker() -> None:
        _migration_4_0_0_replace_docker_placeholders(
            manager,
            {
                "SITE_ENV": "APP_ENV",
                "SITE_NAME": "APP_NAME",
                "SITE_PATH_ROOT": "APP_PATH_ROOT",
            },
        )

        _migration_4_0_0_replace_docker_mapping(
            manager,
            {
                # Moving files from root to env dir.
                "dockerfile: ./docker/": "dockerfile: ${RUNTIME_PATH_APP_ENV}docker/"
            },
        )

    prompt_progress_steps(
        kernel,
        [
            _migration_4_0_0_env,
            _migration_4_0_0_config,
            _migration_4_0_0_dir,
            _migration_4_0_0_move_root_environment_files,
            _migration_4_0_0_move_project_files,
            _migration_4_0_0_update_docker,
        ],
    )


def _migration_4_0_0_et_docker_files(manager: AppAddonManager) -> None:
    env_dir = f"{manager.app_dir}{APP_DIR_APP_DATA}"

    # Convert docker files.
    docker_dir = f"{env_dir}docker/"

    return glob.glob(f"{docker_dir}docker-compose.*")


def _migration_4_0_0_replace_placeholders(file_path: str, replacement_mapping: dict) -> None:
    if not os.path.exists(file_path):
        return

    # Read the file content
    with open(file_path, "r") as f:
        content = f.read()

    # Replace strings based on the mapping dictionary
    for old_str, new_str in replacement_mapping.items():
        content = content.replace(str(old_str), str(new_str))

    # Override the file with updated content
    with open(file_path, "w") as f:
        f.write(content)


def _migration_4_0_0_replace_docker_placeholders(
    manager: AppAddonManager, replacement_mapping: dict
) -> None:
    converted_mapping = {}

    for old_str, new_str in replacement_mapping.items():
        converted_mapping["${" + str(old_str) + "}"] = "${" + str(new_str) + "}"

    _migration_4_0_0_replace_docker_mapping(manager, converted_mapping)


def _migration_4_0_0_replace_docker_mapping(
    manager: AppAddonManager, replacement_mapping: dict
) -> None:
    docker_files = _migration_4_0_0_et_docker_files(manager)

    # Raw file replacements
    # Loop through each docker-compose file
    for docker_file in docker_files:
        _migration_4_0_0_replace_placeholders(docker_file, replacement_mapping)


def is_version_4_0_0(kernel: "Kernel", path: str) -> Optional[bool]:
    if os.path.isdir(path + ".wex"):
        if os.path.isfile(path + ".wex/config"):
            return True

    return None
