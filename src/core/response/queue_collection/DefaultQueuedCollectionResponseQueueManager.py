import yaml

from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager \
    import AbstractQueuedCollectionResponseQueueManager
from abc import ABC

from src.helper.args import arg_replace
from src.helper.process import process_post_exec_function


class DefaultQueuedCollectionResponseQueueManager(AbstractQueuedCollectionResponseQueueManager, ABC):
    def __init__(self, response):
        super().__init__(response)

    def get_previous_value(self):
        path = self.get_previous_response_path()

        if path is None:
            return None

        path = '-'.join(map(str, path))
        previous_data = self.response.kernel.task_file_load(
            path + '.response')

        return yaml.safe_load(previous_data)['body'] if previous_data else None

    def enqueue_next_step_by_index(self, next_step_index):
        super().enqueue_next_step_by_index(next_step_index)

        root = self.response.get_root_parent()
        args = root.request.args.copy()
        arg_replace(args, 'command-request-step', self.response.path_manager.build_step_path())

        process_post_exec_function(
            self.response.kernel,
            root.request.function,
            args
        )

    def enqueue_next_step_if_exists(self, step_index, response) -> bool:
        # Array is modified in super call
        steps_current = list(self.response.path_manager.steps)
        exists = super().enqueue_next_step_if_exists(step_index, response)

        if exists:
            serialized = response.print(interactive_data=False)
            if serialized is not None:
                path = steps_current[:self.response.step_position + 1]
                path = '-'.join(map(str, path))

                # Store response in a file to allow next step to access it.
                self.response.kernel.task_file_write(
                    path + '.response',
                    yaml.dump({
                        # Save raw value to keep type
                        'body': response.first()
                    })
                )

        return exists
