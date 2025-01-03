from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command
from src.decorator.option import option
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option("--path", "-p", type=str, required=False, default=None, help="Argument")
def default__python__init_dirs(kernel: "Kernel", path: Optional[str] = None) -> None:
    import os

    if path is None:
        path = os.getcwd()

    for root, dirs, files in os.walk(path):
        if '__init__.py' not in files:
            init_file_path = os.path.join(root, '__init__.py')

            with open(init_file_path, 'w'):
                pass

            kernel.io.log(f"Created: {init_file_path}")
