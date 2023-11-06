from abc import ABC

from src.core.response.queue_manager.AbstractQueuedCollectionResponseQueueManager \
    import AbstractQueuedCollectionResponseQueueManager
from src.core.response.QueuedCollectionStopResponse import QueuedCollectionStopResponse


class FastModeQueuedCollectionResponseQueueManager(AbstractQueuedCollectionResponseQueueManager, ABC):
    def __init__(self, response):
        super().__init__(response)

    def get_previous_value(self):
        if self.response.kernel.previous_response:
            # Serialize previous data to keep consistency with non-fast mode.
            return self.response.kernel.previous_response.print(
                interactive_data=False
            )

    def render_content_complete(self):
        if self.response.parent:
            self.response.parent.has_next_step = self.response.has_next_step
        # This is the root collection
        else:
            while self.response.has_next_step and not isinstance(self.response.first(), QueuedCollectionStopResponse):
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

        return self.response