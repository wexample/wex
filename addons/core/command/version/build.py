import os

import click
from src.const.globals import GITHUB_GROUP, GITHUB_PROJECT
from src.const.error import ERR_ENV_VAR_MISSING

from addons.default.command.version.increment import default_version_increment
from addons.default.command.config.change import default_config_change


@click.command()
@click.pass_obj
def core_version_build(kernel) -> None:
    print(f'Building new version from {kernel.version}...')

    # Check requirements : GitHub token for changelog build
    env_core_github_token: str = os.getenv('CORE_GITHUB_TOKEN')
    if not env_core_github_token:
        kernel.error(ERR_ENV_VAR_MISSING)

    new_version = default_version_increment.callback(
        kernel.version,
        'dev'
    )

    # Let's start

    # Save new version
    print(f'New version : {new_version}')
    default_config_change.callback(
        kernel.path['root'] + 'src/const/globals.py',
        'WEX_VERSION',
        f"'{new_version}'"
    )

    # Changelog
    print('Building CHANGELOG.md...')
    kernel.shell_exec(
        f'github_changelog_generator -u {GITHUB_GROUP} -p {GITHUB_PROJECT} -t {env_core_github_token}'
    )

