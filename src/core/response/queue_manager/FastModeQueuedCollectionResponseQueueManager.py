from src.core.response.queue_manager.AbstractQueuedCollectionResponseQueueManager \
    import AbstractQueuedCollectionResponseQueueManager


class FastModeQueuedCollectionResponseQueueManager(AbstractQueuedCollectionResponseQueueManager):
    def __init__(self, response):
        super().__init__(response)

    def render_content_complete(self):
        pass