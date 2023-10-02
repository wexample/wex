
from addons.core.command.logs.rotate import core__logs__rotate
from src.decorator.alias import alias
from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Uninstall core")
@alias('cleanup')
def core__core__cleanup(kernel: Kernel):
    kernel.run_function(
        core__logs__rotate,
        {
            'max-days': False,
            'max-count': False
        }
    )

    kernel.rebuild()
