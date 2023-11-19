from addons.app.helper.app import app_create_manager
from src.const.globals import CORE_COMMAND_NAME
from src.core import Kernel
from addons.default.helper.migration import version_guess
from addons.app.decorator.app_command import app_command


@app_command(help="Description", dir_required=False)
def app__version__get(kernel: Kernel, app_dir: str | None = None):
    manager = app_create_manager(kernel, app_dir)
    app_dir = manager.app_dir

    app_version_string = None
    try:
        # Trust regular config file
        app_version_string = manager.config[CORE_COMMAND_NAME]['version']
    except Exception:
        pass

    return app_version_string or version_guess(kernel, app_dir)
