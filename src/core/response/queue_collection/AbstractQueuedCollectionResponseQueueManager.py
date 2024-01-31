from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from src.const.types import BasicInlineValue

if TYPE_CHECKING:
    from src.core.response.AbstractResponse import AbstractResponse
    from src.core.response.QueuedCollectionResponse import (
        QueuedCollectionResponse,
        QueuedCollectionStepsList,
    )


class AbstractQueuedCollectionResponseQueueManager:
    def __init__(self, response: "QueuedCollectionResponse") -> None:
        self.response: "QueuedCollectionResponse" = response

    def render_content_complete(
        self, response: Optional["AbstractResponse"] = None
    ) -> "QueuedCollectionResponse":
        return response or self.response

    @abstractmethod
    def get_previous_value(self) -> BasicInlineValue:
        pass

    def get_previous_response_path(self) -> Optional["QueuedCollectionStepsList"]:
        path_manager = self.response.get_path_manager()
        step_index = path_manager.steps[self.response.step_position]

        # The index is 0
        if step_index == 0:
            # But it has a parent collection
            if self.response.step_position > 0:
                # Get the parent index
                path = path_manager.steps[: self.response.step_position]
                previous_index = path[-1]

                # And parent has a previous item.
                if (
                    previous_index is not None
                    and previous_index > 0
                    and path[-1] is not None
                ):
                    path[-1] -= 1

                    return path
        # The response have a previous one, in the same collection
        else:
            path = path_manager.steps[: self.response.step_position + 1]
            # Ensure the last element is not None before decrementing
            if path[-1] is not None:
                path[-1] -= 1
                return path

        return None

    def get_next_step_index(self, step_index: int) -> bool | int:
        next_index = step_index + 1
        if next_index < len(self.response.collection):
            return next_index

        return False

    def enqueue_next_step_if_exists(
        self, step_index: int, response: "AbstractResponse"
    ) -> bool:
        next_index = self.get_next_step_index(step_index)
        if next_index:
            self.enqueue_next_step_by_index(next_index)

            return True
        return False

    def enqueue_next_step_by_index(self, next_step_index: int) -> None:
        path_manager = self.response.get_path_manager()
        path_manager.steps[self.response.step_position] = next_step_index
        # Remove obsolete parts.
        del path_manager.steps[self.response.step_position + 1 :]
        self.response.has_next_step = True
