from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Return command to run when entering main container", command_type=COMMAND_TYPE_SERVICE,
             should_run=True)
@option('--container', '-c', type=str, required=False, help="Target container")
def php__app__exec(kernel: 'Kernel', app_dir: str, service: str, container: None):
    # Prevent returning data when entering another container.
    if container == service:
        return ['cd', '/var/www/html']
    return None
