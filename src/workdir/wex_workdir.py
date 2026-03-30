from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class
from wexample_wex_addon_app.workdir.app_workdir import AppWorkdir
from wexample_wex_core.workdir.kernel_workdir import KernelWorkdir


@base_class
class WexWorkdir(
    AppWorkdir,
    KernelWorkdir
):
    """
    The main wex core kernel is also an app kernel (with .wex config, etc.)
    """

    def apply(self, **kwargs):
        # AppWorkdir.apply() delegates to manager_run_command (app-manager subprocess).
        # WexWorkdir is the kernel itself — skip to the filestate apply directly.
        return super(AppWorkdir, self).apply(**kwargs)
