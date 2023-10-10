from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from src.core.Kernel import Kernel


class TestKernel(Kernel):
    # Post-exec script should be tested with
    # dedicated subprocesses during tests
    fast_mode = True
    verbosity: int = VERBOSITY_LEVEL_MAXIMUM
