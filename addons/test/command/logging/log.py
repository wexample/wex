from src.decorator.command import command
from src.decorator.option import option
from src.const.globals import COMMAND_TYPE_ADDON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option('--depth', '-d', type=int, default=0, required=False, help="Depth")
def test__logging__log(kernel: 'Kernel', depth: int = 0):
    if depth < 10:
        return kernel.run_function(
            test__logging__log,
            {
                'depth': depth + 1
            }
        )

    return kernel.logger.log_data
