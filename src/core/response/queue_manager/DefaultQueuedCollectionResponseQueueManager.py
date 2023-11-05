from src.core.response.queue_manager.AbstractQueuedCollectionResponseQueueManager \
    import AbstractQueuedCollectionResponseQueueManager


class DefaultQueuedCollectionResponseQueueManager(AbstractQueuedCollectionResponseQueueManager):
    def __init__(self, response):
        super().__init__(response)

    def has_previous_value(self) -> bool:
        return True

    def get_previous_value(self):
        return None