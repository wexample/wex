from abc import abstractmethod


class AbstractQueuedCollectionResponseQueueManager:
    def __init__(self, response):
        self.response = response

    def render_content_complete(self):
        pass

    @abstractmethod
    def has_previous_value(self):
        pass

    @abstractmethod
    def get_previous_value(self):
        pass

    def enqueue_next_step_by_index(self, next_step_index):
        self.response.request.steps[self.response.step_position] = next_step_index
        # Remove obsolete parts.
        del self.response.request.steps[self.response.step_position + 1:]
        self.response.has_next_step = True
