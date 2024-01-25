from src.core.KernelChild import KernelChild


class DefaultModel(KernelChild):
    def __init__(self, name: str, kernel: "Kernel"):
        super().__init__(kernel)

        self.name: str = name

        # We should start ollama container
