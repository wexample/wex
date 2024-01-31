from abc import ABC
from typing import TYPE_CHECKING, cast, Optional

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

    def render_content_complete(self, response: Optional[AbstractResponse] = None) -> "QueuedCollectionResponse":
        from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse

        response = response or self.response
        if response.parent:
            if isinstance(response.parent, QueuedCollectionResponse):
                response.parent.has_next_step = response.has_next_step
        # This is the root collection
        else:
            while (
                isinstance(response, QueuedCollectionResponse)
                and response.has_next_step
                and not isinstance(response.first(), QueuedCollectionStopResponse)
            ):
                response.has_next_step = False
                response.kernel.current_response = None

                args = response.get_request().get_args_list().copy()

                new_response = response.kernel.run_command(
                    response.get_request().get_string_command(), args
                )

                # In fast mode we merge all outputs in the root output bag
                response.output_bag += new_response.output_bag

                # Continue if sub response is not complete
                if new_response.has_next_step:
                    response.has_next_step = True

        return super().render_content_complete(response)
