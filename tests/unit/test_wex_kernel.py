from __future__ import annotations

from types import SimpleNamespace

from wexample_wex_core.common.kernel import Kernel

from src.common.wex import Wex


class TestWexKernel:
    def test_is_a_kernel(self) -> None:
        assert issubclass(Wex, Kernel)

    def test_workdir_state_manager_class(self) -> None:
        from src.workdir.wex_workdir import WexWorkdir

        assert Wex._get_workdir_state_manager_class(SimpleNamespace()) is WexWorkdir


class TestWexLogo:
    def test_logo_includes_kernel_version(self) -> None:
        logo = Wex.get_logo(SimpleNamespace(get_version=lambda: "1.2.3"))

        assert "v1.2.3" in logo

    def test_logo_renders(self) -> None:
        logo = Wex.get_logo(SimpleNamespace())

        assert isinstance(logo, str)
        assert logo


class TestWexWorkdir:
    def test_inheritance(self) -> None:
        from wexample_wex_addon_app.workdir.code_base_workdir import CodeBaseWorkdir
        from wexample_wex_core.workdir.kernel_workdir import KernelWorkdir

        from src.workdir.wex_workdir import WexWorkdir

        assert issubclass(WexWorkdir, CodeBaseWorkdir)
        assert issubclass(WexWorkdir, KernelWorkdir)
