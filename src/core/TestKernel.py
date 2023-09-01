from src.core.Kernel import Kernel


class TestKernel(Kernel):
    test_manager = None

    def setup_test_manager(self, test_manager):
        self.test_manager = test_manager
