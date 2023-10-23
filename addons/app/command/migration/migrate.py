import os
import click

from addons.default.helpers.version import is_greater_than
from addons.default.command.version.parse import default__version__parse
from addons.default.helpers.migration import version_guess, get_migrations_files, migration_exec, \
    MIGRATION_MINIMAL_VERSION, extract_version_from_file_name
from addons.app.helpers.app import create_manager
from src.helper.core import core_kernel_get_version
from src.const.globals import CORE_COMMAND_NAME
from src.decorator.option import option
from src.core import Kernel
from addons.app.decorator.app_command import app_command


@app_command(help="Description", dir_required=False)
@option('--from-version', '-f', type=str, required=False, help="Force initial version number")
@option('--yes', '-y', type=bool, is_flag=True, required=False, help="Do not ask for confirmation")
def app__migration__migrate(kernel: Kernel, app_dir: str|None = None, from_version: str = None, yes: bool = False):
    manager = create_manager(kernel, app_dir)
    app_dir = manager.app_dir

    if from_version:
        app_version_string = from_version
    else:
        app_version_string = None
        try:
            # Trust regular config file
            app_version_string = manager.config[CORE_COMMAND_NAME]['version']
        except Exception:
            pass

    app_version_string = app_version_string or version_guess(kernel, app_dir)

    app_version = kernel.run_function(
        default__version__parse,
        {
            'version': app_version_string
        }
    ).first()

    # Unable to parse version number.
    if not app_version:
        app_version_string = MIGRATION_MINIMAL_VERSION

        app_version = kernel.run_function(
            default__version__parse,
            {
                'version': app_version_string
            }
        ).first()

    if not yes and not click.confirm(
            f'Are you ready to migrate {manager.get_config("global.name")} from version {app_version_string}',
            default=True):
        return False

    # Create an empty config
    if manager.config == {}:
        # Only create config but do not save it
        # until migration is completed
        manager.config = manager.create_config(
            os.path.basename(
                os.path.normpath(app_dir)
            )
        )

    kernel.io.log(f'Current version defined as {app_version_string}')
    print(manager.config)

    for migration_file in get_migrations_files(kernel):
        migration_version_string = extract_version_from_file_name(migration_file)
        print(migration_file)
        print(migration_version_string)

        migration_version = kernel.run_function(
            default__version__parse,
            {
                'version': migration_version_string
            }
        ).first()

        if is_greater_than(migration_version, app_version):
            kernel.io.log(f'Migrating to {migration_version_string}')

            migration_exec(
                kernel,
                migration_version_string,
                'migration',
                [manager]
            )

            print('...')
            print(os.path.exists('/builds/'))
            print(os.path.exists('/builds/wexample/'))
            print(os.path.exists('/builds/wexample/wex/'))
            print(os.path.exists('/builds/wexample/wex/tmp/'))
            print(os.path.exists('/builds/wexample/wex/tmp/tests/'))
            print(os.path.exists('/builds/wexample/wex/tmp/tests/3.0.0/'))
            print(os.path.exists('/builds/wexample/wex/tmp/tests/3.0.0/.wex/'))
            print(os.path.exists('/builds/wexample/wex/tmp/tests/3.0.0/.wex/config.yml'))

            manager.set_config(
                f'{CORE_COMMAND_NAME}.version',
                migration_version_string
            )

            print('...')

            app_version = migration_version

    manager.set_config(
        f'{CORE_COMMAND_NAME}.version',
        core_kernel_get_version(kernel)
    )
    kernel.io.message(f'Migration complete')
