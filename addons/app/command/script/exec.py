from src.decorator.option import option
from src.core import Kernel
from addons.app.decorator.app_command import app_command


@app_command(help="Description")
@option('--name', '-n', type=str, required=True, help="Script name")
def app__script__exec(kernel: Kernel, app_dir: str, name: str):


    return None
