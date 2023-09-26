import git
import os
from addons.default.command.version.increment import default__version__increment
from addons.app.command.version.build import app__version__build
from addons.app.command.config.set import app__config__set
from addons.app.const.app import APP_FILEPATH_REL_CONFIG
from src.const.error import ERR_CORE_REPO_DIRTY
from src.const.globals import FILE_VERSION, FILE_README, CORE_COMMAND_NAME
from src.helper.core import core_kernel_get_version
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option


@command(help="Build a new version of current core, or commit new version changes")
@option('--commit', '-ok', required=False, is_flag=True, default=False,
        help="New version changes has been validated, ask to commit changes")
def core__version__build(kernel: Kernel, commit: bool = False) -> None:
    version = core_kernel_get_version(kernel)
    repo = git.Repo(kernel.path['root'])

    if not commit:
        current_version = core_kernel_get_version(kernel)
        kernel.log(f'Building new version from {current_version}...')

        # There is no uncommitted change
        if repo.is_dirty(untracked_files=True):
            kernel.error(ERR_CORE_REPO_DIRTY, {
                'diff': repo.git.diff()
            })

        new_version = default__version__increment.callback(
            version,
            build=True
        )

        # Write new_version to file
        with open(f'{kernel.path["root"]}{FILE_VERSION}', 'w') as version_file:
            version_file.write(str(new_version))

        # Set wex version for itself.
        kernel.run_function(
            app__config__set,
            {
                'key': 'wex.version',
                'value': new_version
            }
        )

        # Enforce new version for wex app.
        kernel.run_function(
            app__version__build,
            {
                'version': new_version,
                'app-dir': kernel.path['root']
            }
        )

        # Update README.md
        readme_path = os.path.join(kernel.path["root"], FILE_README)

        with open(readme_path, 'r') as file:
            readme_content = file.read()

        # Replace old version with new version
        updated_content = readme_content.replace('wex v' + version, 'wex v' + new_version)

        with open(readme_path, 'w') as file:
            file.write(updated_content)

        kernel.message_next_command(
            core__version__build,
            {
                'commit': True
            }
        )

    else:
        if not repo.is_dirty(untracked_files=True):
            kernel.log('No changes to commit')
            return

        repo.index.add(kernel.path['root'] + FILE_VERSION)
        repo.index.add(kernel.path['root'] + FILE_README)
        repo.index.add(kernel.path['root'] + APP_FILEPATH_REL_CONFIG)

        kernel.run_function(
            app__version__build,
            {
                'commit': commit,
                'app-dir': kernel.path['root']
            }
        )
