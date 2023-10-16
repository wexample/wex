from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option


@command(help="Return command to run when entering main container")
@app_dir_option()
@service_option()
@option('--container', '-c', type=str, required=False, help="Target container")
def php__app__exec(kernel: Kernel, app_dir: str, service: str, container: None):
    # Prevent returning data when entering another container.
    if container == service:
        return ['cd', '/var/www/html']
    return None
