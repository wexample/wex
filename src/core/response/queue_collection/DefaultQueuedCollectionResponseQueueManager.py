from abc import ABC
from typing import TYPE_CHECKING, cast

import yaml

from src.const.types import BasicInlineValue
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.helper.args import args_replace_one
from src.helper.process import process_post_exec_function

if TYPE_CHECKING:
    from src.core.response.AbstractResponse import AbstractResponse
    from src.core.response.QueuedCollectionResponse import (
        QueuedCollectionResponse,
        QueuedCollectionStepsList,
    )


class DefaultQueuedCollectionResponseQueueManager(
    AbstractQueuedCollectionResponseQueueManager, ABC
):
    def __init__(self, response: "QueuedCollectionResponse") -> None:
        super().__init__(response)

    def get_previous_storage_path(self) -> str | None:
        path = self.get_previous_response_path()

        if path is None:
            return None

        return self.build_storage_path(path)

    def get_previous_value(self) -> BasicInlineValue:
        storage_path = self.get_previous_storage_path()

        if not storage_path:
            return None

        previous_data = self.response.kernel.task_file_load(
            storage_path, delete_after_read=False
        )

        return yaml.safe_load(previous_data)["body"] if previous_data else None

    def enqueue_next_step_by_index(self, next_step_index: int) -> None:
        super().enqueue_next_step_by_index(next_step_index)

        root = self.response.get_root_parent()
        args = root.get_request().get_args_list_copy()

        args_replace_one(
            arg_list=args,
            arg_name="command-request-step",
            value=self.response.get_path_manager().build_step_path(),
        )

        process_post_exec_function(
            self.response.kernel, root.get_request().get_string_command(), args
        )

    def build_storage_path(self, path: "QueuedCollectionStepsList") -> str:
        return "-".join(map(str, path)) + ".response"

    def enqueue_next_step_if_exists(
        self, step_index: int, response: "AbstractResponse"
    ) -> bool:
        # Array is modified in super call
        steps_current = self.response.get_path_manager().steps.copy()
        exists = super().enqueue_next_step_if_exists(step_index, response)
        storage_path = cast(
            "QueuedCollectionStepsList",
            steps_current[: self.response.step_position + 1],
        )

        if exists:
            store_data = response.store_data()
            if store_data is not None:
                # Store response in a file to allow next step to access it.
                self.response.kernel.task_file_write(
                    self.build_storage_path(storage_path),
                    yaml.dump(
                        {
                            # Save raw value to keep type
                            "body": store_data
                        }
                    ),
                )
        else:
            previous_storage_path = self.get_previous_storage_path()

            if previous_storage_path:
                self.response.kernel.task_file_load(previous_storage_path)

        return exists
