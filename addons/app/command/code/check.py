from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(
    help="Validate the code of current application", command_type=COMMAND_TYPE_ADDON
)
def app__code__check(kernel: "Kernel", app_dir: str) -> None:
    """
    This method is a placeholder to allow local app command attachment.s
    """
    return None
