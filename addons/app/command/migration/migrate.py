import os

from addons.default.helpers.version import is_greater_than
from addons.default.command.version.parse import default__version__parse
from addons.app.decorator.app_dir_optional import app_dir_optional
from addons.app.command.location.find import app__location__find
from addons.app.AppAddonManager import AppAddonManager
from addons.default.helpers.migration import version_guess, get_migrations_files, migration_exec, \
    MIGRATION_MINIMAL_VERSION
from src.helper.core import core_kernel_get_version
from src.const.globals import CORE_COMMAND_NAME
from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel


@command(help="Description")
@app_dir_optional
@option('--app-dir', '-a', type=str, required=False, help="App directory")
@option('--from-version', '-f', type=str, required=False, help="Force initial version number")
def app__migration__migrate(kernel: Kernel, app_dir: str = None, from_version: str = None):
    if not app_dir:
        app_dir = kernel.run_function(app__location__find).first()

        if not app_dir:
            app_dir = os.getcwd() + os.sep

    # Create a dedicated manager
    manager = AppAddonManager(kernel, 'app-migration')
    manager.set_app_workdir(app_dir)

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

    for migration_file in get_migrations_files(kernel):
        migration_version_string = migration_file.replace(".py", "")

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

            manager.set_config(
                f'{CORE_COMMAND_NAME}.version',
                migration_version_string
            )
            app_version = migration_version

    manager.set_config(
        f'{CORE_COMMAND_NAME}.version',
        core_kernel_get_version(kernel)
    )
    kernel.io.message(f'Migration complete')
