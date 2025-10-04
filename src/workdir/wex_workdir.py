from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class
from wexample_wex_addon_app.workdir.mixin.app_workdir_mixin import AppWorkdirMixin
from wexample_wex_core.workdir.kernel_workdir import KernelWorkdir


@base_class
class WexWorkdir(
    AppWorkdirMixin,
    KernelWorkdir
):
    """
    The main wex core kernel is also an app kernel (with .wex config, etc.)
    """
