from src.core.response.TableResponse import TableResponse
from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON


@command(help="Return a table response", command_type=COMMAND_TYPE_ADDON)
@option('--arg', '-a', type=str, required=True, help="Argument")
def test__return_type__table_response(kernel: Kernel, arg):
    return TableResponse(
        kernel,
        'Test table',
        [
            ['lorem', 'ipsum', 'dolor', 'sit', 'amet'],
            [1, 2, 3, 4, 5.6],
            ['shorten', 'line'],
            [True, False, None],
            [arg, arg, arg, arg]
        ])
