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
