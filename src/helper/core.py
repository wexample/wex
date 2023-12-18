from __future__ import annotations

import os
from typing import TYPE_CHECKING

from src.const.globals import FILE_VERSION
from src.helper.file import file_read

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def core_dir_get_version(core_dir: str) -> str:
    return file_read(f"{core_dir}{FILE_VERSION}").strip()


def core_kernel_get_version(kernel: "Kernel") -> str:
    return core_dir_get_version(kernel.directory.path)


def core_get_daemon_service_resource_path(kernel: "Kernel") -> str:
    return os.path.join(kernel.directory.path, "src", "resources", "wexd.service")
