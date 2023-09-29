from src.core.Kernel import Kernel


class TestKernel(Kernel):
    # Post-exec script cannot be tested with unitest.
    fast_mode = True
