from src.decorator.command import command
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON
from src.core.response.KeyValueResponse import KeyValueResponse


@command(help="Return a key / value response", command_type=COMMAND_TYPE_ADDON)
def test__return_type__key_value(kernel: Kernel):
    return KeyValueResponse(kernel, {
        'str': 'lorem',
        'int': 123,
        'bool': True
    })
