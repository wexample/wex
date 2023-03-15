import os
import git
import click
from src.const.globals import GITHUB_GROUP, GITHUB_PROJECT, WEX_VERSION
from src.const.error import ERR_CORE_REPO_DIRTY, ERR_ENV_VAR_MISSING
import subprocess
from addons.default.command.version.increment import default_version_increment
from addons.core.command.globals.set import core_globals_set


def has_uncommitted_changes(directory):
    command = 'git status --porcelain'
    output = subprocess.check_output(command.split(), cwd=directory).decode()
    return bool(output.strip())


@click.command
@click.pass_obj
def core_version_build(kernel) -> None:
    kernel.log(f'Building new version from {kernel.version}...')

    # Check requirements
    # GitHub token for changelog build
    env_core_github_token: str = os.getenv('CORE_GITHUB_TOKEN')
    if not env_core_github_token:
        kernel.error(ERR_ENV_VAR_MISSING)

    # There is no uncommitted change
    repo = git.Repo(kernel.path['root'])
    if repo.is_dirty(untracked_files=True):
        kernel.error(ERR_CORE_REPO_DIRTY, {
            'diff': repo.git.diff()
        })

    new_version = default_version_increment.callback(
        kernel.version,
    )

    # Let's start

    # Save new version
    kernel.log(f'New version : {new_version}')
    kernel.exec_function(
        core_globals_set,
        {
            'key': 'WEX_VERSION',
            'value': new_version
        }
    )

    # Enforce new version for wex app.
    kernel.exec(
        'app::version/build',
        {
            'version': new_version,
            'app_dir': kernel.path['root']
        }
    )

    # Changelog
    kernel.log('Building CHANGELOG.md...')
    kernel.shell_exec(
        f'github_changelog_generator -u {GITHUB_GROUP} -p {GITHUB_PROJECT} -t {env_core_github_token}'
    )
