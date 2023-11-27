from abc import abstractmethod

from src.core.response.AbstractResponse import AbstractResponse


class AbstractQueuedCollectionResponseQueueManager:
    def __init__(self, response: AbstractResponse) -> None:
        self.response: AbstractResponse = response

    def render_content_complete(self) -> AbstractResponse:
        return self.response

    @abstractmethod
    def get_previous_value(self):
        pass

    def get_previous_response_path(self) -> list | None:
        step_index = self.response.path_manager.steps[self.response.step_position]

        # The index is 0
        if step_index == 0:
            # But it has a parent collection
            if self.response.step_position > 0:
                # Get the parent index
                path = self.response.path_manager.steps[: self.response.step_position]
                previous_index = path[-1]

                # And parent has a previous item.
                if previous_index > 0:
                    path[-1] -= 1

                return path
            else:
                return None
        # The response have a previous one, in the same collection
        else:
            path = self.response.path_manager.steps[: self.response.step_position + 1]
            path[-1] -= 1

            return path

    def get_next_step_index(self, step_index) -> bool | int:
        next_index = step_index + 1
        if next_index < len(self.response.collection):
            return next_index

        return False

    def enqueue_next_step_if_exists(self, step_index, response) -> bool:
        next_index = self.get_next_step_index(step_index)
        if next_index:
            self.enqueue_next_step_by_index(next_index)

            return True
        return False

    def enqueue_next_step_by_index(self, next_step_index):
        self.response.path_manager.steps[self.response.step_position] = next_step_index
        # Remove obsolete parts.
        del self.response.path_manager.steps[self.response.step_position + 1 :]
        self.response.has_next_step = True
