import os
import shutil

from addons.core.command.logs.rotate import core__logs__rotate
from src.decorator.alias import alias
from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Uninstall core")
@alias('cleanup')
def core__core__cleanup(kernel: Kernel):
    shutil.rmtree(kernel.path['tmp'])

    os.makedirs(os.path.dirname(kernel.path['tmp']), exist_ok=True)
    gitkeep_path = os.path.join(kernel.path['tmp'], '.gitkeep')

    kernel.rebuild()
