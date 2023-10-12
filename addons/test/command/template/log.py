from src.decorator.command import command
from src.core import Kernel


@command(help="Description")
def test__template__log(kernel: Kernel):
    kernel.io.log('Simple log')
    kernel.io.message('Simple message')
    kernel.io.success('Simple success')
    kernel.io.fail('Simple fail')

    return 'COMPLETE'
