from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


def core_dir_get_version(core_dir: str) -> str:
    from src.const.globals import FILE_VERSION
    from wexample_helpers.helpers.file import file_read
    return file_read(f"{core_dir}{FILE_VERSION}").strip()


def core_get_daemon_service_resource_path(kernel: Kernel) -> str:
    return os.path.join(kernel.directory.path, "src", "resources", "wexd.service")


def core_kernel_get_version(kernel: Kernel) -> str:
    return core_dir_get_version(kernel.directory.path)
