from addons.app.helpers.app import create_manager
from src.const.globals import CORE_COMMAND_NAME
from src.decorator.command import command
from src.core import Kernel
from addons.default.helpers.migration import version_guess
from addons.app.decorator.app_dir_optional import app_dir_optional
from src.decorator.option import option


@command(help="Description")
@app_dir_optional
@option('--app-dir', '-a', type=str, required=False, help="App directory")
def app__version__get(kernel: Kernel, app_dir: str | None = None):
    manager = create_manager(kernel, app_dir)
    app_dir = manager.app_dir

    app_version_string = None
    try:
        # Trust regular config file
        app_version_string = manager.config[CORE_COMMAND_NAME]['version']
    except Exception:
        pass

    return app_version_string or version_guess(kernel, app_dir)
