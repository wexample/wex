from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command
from typing import TYPE_CHECKING
from src.decorator.alias import alias
from addons.app.command.env.choose import app__env__choose

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias("configure")
@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def core__configure__all(kernel: "Kernel") -> None:
    kernel.run_function(
        app__env__choose,
        {
            "app_dir": kernel.directory.path,
            "question": "Choose global server environment"
        })
