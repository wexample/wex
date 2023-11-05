from abc import abstractmethod


class AbstractQueuedCollectionResponseQueueManager:
    def __init__(self, response):
        self.response = response

    def render_content_complete(self):
        pass

    @abstractmethod
    def get_previous_value(self):
        pass

    def enqueue_next_step_if_exists(self, step_index, response) -> bool:
        next_index = step_index + 1
        if next_index < len(self.response.collection):
            self.enqueue_next_step_by_index(next_index)

            return True
        return False

    def enqueue_next_step_by_index(self, next_step_index):
        self.response.request.steps[self.response.step_position] = next_step_index
        # Remove obsolete parts.
        del self.response.request.steps[self.response.step_position + 1:]
        self.response.has_next_step = True
