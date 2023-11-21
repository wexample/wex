import os
from typing import Optional

from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

@app_command(
    dir_required=False,
    help="Search for the config file in the given directory path or its parent directories.")
@option('--recursive', '-r', type=bool, required=False, default=True,
        help="App directory")
def app__location__find(kernel: 'Kernel', app_dir: Optional[str] = False, recursive: bool = True) -> Optional[str]:
    """Search for the config file in the given directory path or its parent directories.
    Returns the path of the directory containing the config file, or None if not found.
    """

    manager = kernel.addons['app']

    if not app_dir:
        app_dir = os.getcwd()
    else:
        app_dir = os.path.abspath(app_dir)

    # Avoid loops when passing //
    app_dir = os.path.realpath(app_dir)

    while app_dir != '/':  # Stop at root directory
        if not os.path.exists(app_dir):
            return None

        if manager.is_app_root(app_dir):
            return f'{app_dir}{os.sep}'

        if not recursive:
            return None

        app_dir = os.path.dirname(app_dir)
    return None
