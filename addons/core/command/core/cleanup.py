import os
import shutil

from src.decorator.alias import alias
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.no_log import no_log
from addons.system.command.own.this import system__own__this


@command(help="Uninstall core")
@no_log()
@alias('cleanup')
def core__core__cleanup(kernel: Kernel):
    tmp_dir = kernel.get_or_create_path('tmp')
    shutil.rmtree(tmp_dir)

    os.makedirs(os.path.dirname(tmp_dir), exist_ok=True)
    with open(os.path.join(tmp_dir, '.gitkeep'), 'a'):
        pass

    kernel.rebuild()

    # Reset perms
    kernel.run_function(
        system__own__this,
        {
            'path': kernel.get_path('root')
        }
    )
