from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from src.utils.kernel import Kernel


class TestKernel(Kernel):
    # Post-exec script should be tested with
    # dedicated subprocesses during tests
    fast_mode = True
    verbosity: int = VERBOSITY_LEVEL_MAXIMUM
    tty = False

    def __init__(self, entrypoint_path: str, task_id: str | None = None) -> None:
        super().__init__(
            entrypoint_path,
            task_id,
        )
