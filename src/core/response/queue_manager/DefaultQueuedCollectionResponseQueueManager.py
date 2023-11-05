from src.core.response.queue_manager.AbstractQueuedCollectionResponseQueueManager \
    import AbstractQueuedCollectionResponseQueueManager
from abc import ABC

from src.helper.args import arg_replace
from src.helper.process import process_post_exec_function


class DefaultQueuedCollectionResponseQueueManager(AbstractQueuedCollectionResponseQueueManager, ABC):
    def __init__(self, response):
        super().__init__(response)

    def get_previous_value(self):
        return self.response.kernel.task_file_load(self.response.build_step_path() + '.response')

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

    def enqueue_next_step_if_exists(self, step_index, response) -> bool:
        exists = super().enqueue_next_step_if_exists(step_index, response)

        if exists:
            serialized = response.print(interactive_data=False)
            if serialized is not None:
                # Store response in a file to allow next step to access it.
                self.response.kernel.task_file_write(self.response.build_step_path() + '.response', serialized)
