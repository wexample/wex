from src.core.Kernel import Kernel


class TestKernel(Kernel):
    # Post-exec script should be tested with
    # dedicated subprocesses during tests
    fast_mode = True
