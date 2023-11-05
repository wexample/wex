from abc import ABC

from src.core.response.queue_manager.AbstractQueuedCollectionResponseQueueManager \
    import AbstractQueuedCollectionResponseQueueManager
from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse


class FastModeQueuedCollectionResponseQueueManager(AbstractQueuedCollectionResponseQueueManager, ABC):
    def __init__(self, response):
        super().__init__(response)

    def render_content_complete(self):
        if self.response.parent:
            self.response.parent.has_next_step = self.response.has_next_step
        # This is the root collection
        else:
            while self.response.has_next_step and not isinstance(self.response.first(), ResponseCollectionStopResponse):
                self.response.has_next_step = False
                self.response.kernel.previous_response = self.response
                self.response.kernel.current_response = None

                args = self.response.request.args.copy()

                response = self.response.kernel.run_function(
                    self.response.request.function,
                    args
                )

                # In fast mode we merge all outputs in the root output bag.
                self.response.output_bag += response.output_bag