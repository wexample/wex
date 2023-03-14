import os

import click
from src.const.globals import GITHUB_GROUP, GITHUB_PROJECT
from src.const.error import ERR_ENV_VAR_MISSING


@click.command()
@click.pass_obj
def core_version_build(kernel) -> None:
    print(f'Building new version from {kernel.version}...')

    new_version = kernel.exec('default::version/increment', ['--version', '5.0.0', '-t', 'dev'])
    print(f'New version : {new_version}')

    if env_core_github_token:
        print('Building CHANGELOG.md...')

        kernel.shell_exec(
            f'github_changelog_generator -u {GITHUB_GROUP} -p {GITHUB_PROJECT} -t {env_core_github_token}'
        )
    else:
        kernel.error(ERR_ENV_VAR_MISSING)

