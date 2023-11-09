import yaml

from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager \
    import AbstractQueuedCollectionResponseQueueManager
from abc import ABC

from src.helper.args import args_replace_one
from src.helper.process import process_post_exec_function


class DefaultQueuedCollectionResponseQueueManager(AbstractQueuedCollectionResponseQueueManager, ABC):
    def __init__(self, response):
        super().__init__(response)

    def get_previous_storage_path(self) -> str | None:
        path = self.get_previous_response_path()

        if path is None:
            return None

        return self.build_storage_path(path)

    def get_previous_value(self):
        storage_path = self.get_previous_storage_path()

        if not storage_path:
            return None

        previous_data = self.response.kernel.task_file_load(
            storage_path,
            delete_after_read=False
        )

        return yaml.safe_load(previous_data)['body'] if previous_data else None

    def enqueue_next_step_by_index(self, next_step_index):
        super().enqueue_next_step_by_index(next_step_index)

        root = self.response.get_root_parent()
        args = root.request.args.copy()

        args_replace_one(
            arg_list=args,
            arg_name='command-request-step',
            value=self.response.path_manager.build_step_path())

        process_post_exec_function(
            self.response.kernel,
            root.request.command,
            args
        )

    def build_storage_path(self, path: list) -> str:
        return '-'.join(map(str, path)) + '.response'

    def enqueue_next_step_if_exists(self, step_index, response) -> bool:
        # Array is modified in super call
        steps_current = list(self.response.path_manager.steps)
        exists = super().enqueue_next_step_if_exists(step_index, response)
        storage_path = steps_current[:self.response.step_position + 1]

        if exists:
            store_data = response.store_data()
            if store_data is not None:
                # Store response in a file to allow next step to access it.
                self.response.kernel.task_file_write(
                    self.build_storage_path(storage_path),
                    yaml.dump({
                        # Save raw value to keep type
                        'body': store_data
                    })
                )
        else:
            storage_path = self.get_previous_storage_path()

            if storage_path:
                self.response.kernel.task_file_load(
                    storage_path
                )

        return exists
