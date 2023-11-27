from __future__ import annotations

import os
from typing import TYPE_CHECKING

from src.const.globals import FILE_VERSION

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def core_dir_get_version(core_dir: str) -> str:
    with open(f'{core_dir}{FILE_VERSION}', 'r') as file:
        return file.read().strip()


def core_kernel_get_version(kernel: 'Kernel') -> str:
    return core_dir_get_version(kernel.get_path('root'))


def core_get_daemon_service_resource_path(kernel: 'Kernel') -> str:
    return os.path.join(
        kernel.get_path('root'),
        'src',
        'resources',
        'wexd.service'
    )
