import os
import shutil

from src.decorator.alias import alias
from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Uninstall core")
@alias('cleanup')
def core__core__cleanup(kernel: Kernel):
    tmp_dir = kernel.get_or_create_path('tmp')
    shutil.rmtree(tmp_dir)

    os.makedirs(os.path.dirname(tmp_dir), exist_ok=True)
    with open(os.path.join(tmp_dir, '.gitkeep'), 'a'):
        pass

    kernel.rebuild()
