import importlib
import os
import click

from addons.app.command.config.version import app__config__version
from addons.default.helpers.version import is_greater_than, version_join
from addons.default.command.version.parse import default__version__parse
from addons.app.decorator.app_location_optional import app_location_optional
from addons.app.command.location.find import app__location__find
from src.const.error import ERR_UNEXPECTED
from src.core.response.AbortResponse import AbortResponse
from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel


@command(help="Description")
@app_location_optional
@option('--app-dir', '-a', type=str, required=False, help="App directory")
def app__migration__migrate(kernel: Kernel, app_dir: str = None):
    if not app_dir:
        app_dir = kernel.run_function(app__location__find)

    # Get the parsed version of application.
    app_version_string = kernel.run_function(app__config__version)
    app_version = kernel.run_function(
        default__version__parse,
        {
            'version': app_version_string
        }
    )

    if not app_dir:
        app_dir = os.getcwd()
        kernel.message('No application directory found.')
        if not click.confirm(f'Do you want to proceed migration from version {app_version_string} in : {app_dir}?',
                             default=True):
            return AbortResponse(kernel)

    path_migrations = os.path.join(kernel.path['addons'], 'app/migrations') + os.sep

    for item in reversed(os.listdir(path_migrations)):
        migration_version = kernel.run_function(
            default__version__parse,
            {
                'version': item
            }
        )

        if is_greater_than(migration_version, app_version):
            # Create the method name based on item
            version = item.replace(".py", "").replace(".", "_")
            method_name = f"migration_{version}"

            # Dynamically import the module
            module_name = item.replace(".py", "")
            print(method_name)
            spec = importlib.util.spec_from_file_location(module_name, path_migrations + item)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get the method from the module
            method_to_call = getattr(module, method_name, None)

            if method_to_call is None:
                import logging
                kernel.error(
                    ERR_UNEXPECTED,
                    {
                        'error': f"Method {method_name} not found in module {module_name}"
                    },
                    logging.ERROR
                )

                return AbortResponse(kernel)

            kernel.log(f'Migrating to {version_join(migration_version)}')

            # Execute the method
            method_to_call(kernel)

            kernel.message(f'Migration complete to {version_join(migration_version)}')
            app_version = migration_version
