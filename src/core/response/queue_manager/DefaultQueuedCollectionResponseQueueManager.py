from src.core.response.queue_manager.AbstractQueuedCollectionResponseQueueManager \
    import AbstractQueuedCollectionResponseQueueManager
from abc import ABC

from src.helper.args import arg_replace
from src.helper.process import process_post_exec_function


class DefaultQueuedCollectionResponseQueueManager(AbstractQueuedCollectionResponseQueueManager, ABC):
    def __init__(self, response):
        super().__init__(response)

    def has_previous_value(self) -> bool:
        return True

    def get_previous_value(self):
        return None

    def enqueue_next_step_by_index(self, next_step_index):
        super().enqueue_next_step_by_index(next_step_index)

        root = self.response.get_root_parent()
        args = root.request.args.copy()
        arg_replace(args, 'command-request-step', self.response.build_step_path())

        process_post_exec_function(
            self.response.kernel,
            root.request.function,
            args
        )
