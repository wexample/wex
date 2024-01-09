from src.const.globals import COMMAND_TYPE_ADDON
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
def app__test__run(kernel: "Kernel", app_dir: str) -> None:
    return None
