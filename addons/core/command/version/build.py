import git
import click
import re
import os
from addons.default.command.version.increment import default__version__increment
from addons.app.command.version.build import app__version__build
from addons.app.command.config.set import app__config__set
from src.const.error import ERR_CORE_REPO_DIRTY
from src.const.globals import FILE_VERSION
from src.helper.core import core_kernel_get_version


@click.command
@click.pass_obj
@click.option('--commit', '-ok', required=False, is_flag=True, default=False)
def core__version__build(kernel, commit: bool = False) -> None:
    version = core_kernel_get_version(kernel)
    repo = git.Repo(kernel.path['root'])

    if not commit:
        kernel.log(f'Building new version from {version}...')

        # There is no uncommitted change
        if repo.is_dirty(untracked_files=True):
            kernel.error(ERR_CORE_REPO_DIRTY, {
                'diff': repo.git.diff()
            })

        new_version = default__version__increment.callback(
            version,
        )

        kernel.log(f'New version : {new_version}', increment=1)

        # Write new_version to file
        with open(f'{kernel.path["root"]}{FILE_VERSION}', 'w') as version_file:
            version_file.write(str(new_version))

        # Set wex version for itself.
        kernel.exec_function(
            app__config__set,
            {
                'key': 'global.wex_version',
                'value': new_version
            }
        )

        # Enforce new version for wex app.
        kernel.exec_function(
            app__version__build,
            {
                'version': new_version,
                'app-dir': kernel.path['root']
            }
        )

        # Update README.md
        readme_path = os.path.join(kernel.path["root"], 'README.md')

        with open(readme_path, 'r') as file:
            readme_content = file.read()

        # Replace old version with new version
        updated_content = readme_content.replace('wex v' + version, 'wex v' + new_version)

        with open(readme_path, 'w') as file:
            file.write(updated_content)

    else:
        if not repo.is_dirty(untracked_files=True):
            kernel.log('No changes to commit')
            return

        repo.index.add(kernel.path['root'] + FILE_VERSION)

        kernel.exec_function(
            app__version__build,
            {
                'commit': commit,
                'app-dir': kernel.path['root']
            }
        )
