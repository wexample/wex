from src.decorator.command import command
from src.const.globals import COMMAND_TYPE_ADDON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def test__logging__event(kernel: 'Kernel'):
    kernel.logger.append_event(
        'TEST_EVENT_EMPTY'
    )

    kernel.logger.append_event(
        'TEST_EVENT_DATA',
        {
            "string": "lorem",
            "int": 123,
        }
    )
