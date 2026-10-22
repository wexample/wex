from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class
from wexample_wex_addon_app.workdir.code_base_workdir import CodeBaseWorkdir
from wexample_wex_core.workdir.kernel_workdir import KernelWorkdir


@base_class
class WexWorkdir(
    CodeBaseWorkdir,
    KernelWorkdir
):
    """
    Kernel-level workdir for the wex process itself.

    IMPORTANT: this class is NOT what addon commands receive as `app_workdir`.
    When running `wex <command>` from the wex project directory, the `app_workdir`
    resolved by the AppMiddleware is the AppWorkdir defined in:
        .wex/python/app_manager/app_workdir.py

    WexWorkdir is only instantiated as the kernel's own workdir (KernelWorkdir).
    Project-specific overrides (publish, bump, etc.) must go in AppWorkdir, not here.
    """

    def apply(self, **kwargs):
        # CodeBaseWorkdir.apply() delegates to manager_run_command (app-manager subprocess).
        # WexWorkdir is the kernel itself — skip to the filestate apply directly.
        from wexample_wex_addon_app.workdir.managed_workdir import ManagedWorkdir

        return super(ManagedWorkdir, self).apply(**kwargs)

