import time
from typing import TYPE_CHECKING

from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Description")
@option('--arg', '-a', type=str, required=False, help="Test argument")
def test__template__log(kernel: 'Kernel', arg):
    kernel.io.message('Simple first message')
    kernel.io.log('Simple log A')
    kernel.io.log('Simple log B')
    kernel.io.log('Simple log C')
    kernel.io.log('Simple log D')
    kernel.io.log('Simple log E')
    kernel.io.log('Simple log F')
    kernel.io.log('Simple log G')
    kernel.io.log('Simple log H')
    kernel.io.log('Simple log I')
    kernel.io.log('Simple log J')
    kernel.io.log('Simple log K')

    kernel.io.message('Simple message with text', 'This is a text')

    kernel.io.message_next_command(
        test__template__log,
        {
            'arg': 'YES'
        }
    )

    kernel.io.message_all_next_commands(
        [
            test__template__log,
            test__template__log,
            test__template__log,
            test__template__log,
        ],
    )

    for i in range(25):
        kernel.io.log(f'Simple log {str(i)}')
        time.sleep(0.3)

        if i % 10 == 0:
            kernel.io.message(f'Scroll test step {i}')

    kernel.io.success('Simple success')
    kernel.io.fail('Simple fail')

    return 'COMPLETE'
