from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command
from src.decorator.option import option
from typing import TYPE_CHECKING
from addons.app.command.remote.available import app__remote__available

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option(
    "--environment",
    "-e",
    type=str,
    required=True,
    help="Remote environment (dev, prod)",
)
def app__mirror__push(kernel: "Kernel", environment: str) -> None:
    response = kernel.run_function(
        app__remote__available, {
            "environment":
                environment}
    )

    if response.first() is not True:
        return
