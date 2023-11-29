from abc import ABC
from typing import TYPE_CHECKING, cast

from src.const.types import BasicInlineValue
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)

if TYPE_CHECKING:
    from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse


class FastModeQueuedCollectionResponseQueueManager(
    AbstractQueuedCollectionResponseQueueManager, ABC
):
    def __init__(self, response: "QueuedCollectionResponse") -> None:
        super().__init__(response)

    def get_previous_value(self) -> BasicInlineValue:
        self.response.find_parent_response_collection()
        path = self.get_previous_response_path()

        if path is None:
            return None

        previous_response = self.response.get_path_manager().map[
            self.response.get_path_manager().build_step_path(path)
        ]

        first = previous_response.output_bag[0]
        assert isinstance(first, AbstractResponse)
        if previous_response and first.storable_data():
            # Get previous data keeps consistency with non-fast mode.
            return cast(BasicInlineValue, previous_response.first())

        return None

    def render_content_complete(self) -> "QueuedCollectionResponse":
        from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse

        if self.response.parent:
            if isinstance(self.response.parent, QueuedCollectionResponse):
                self.response.parent.has_next_step = self.response.has_next_step
        # This is the root collection
        else:
            while (
                isinstance(self.response, QueuedCollectionResponse)
                and self.response.has_next_step
                and not isinstance(self.response.first(), QueuedCollectionStopResponse)
            ):
                self.response.has_next_step = False
                self.response.kernel.current_response = None

                args = self.response.get_request().get_args_list().copy()

                response = self.response.kernel.run_command(
                    self.response.get_request().get_string_command(), args
                )

                # In fast mode we merge all outputs in the root output bag.
                self.response.output_bag += response.output_bag

        return super().render_content_complete()
