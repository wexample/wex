import os
import shutil

from src.decorator.alias import alias
from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Uninstall core")
@alias('cleanup')
def core__core__cleanup(kernel: Kernel):
    shutil.rmtree(kernel.path['tmp'])

    os.makedirs(os.path.dirname(kernel.path['tmp']), exist_ok=True)
    with open(os.path.join(kernel.path['tmp'], '.gitkeep'), 'a'):
        pass

    kernel.rebuild()
