from __future__ import annotations

from src.core.response.queue_collection.QueuedCollectionPathManager import QueuedCollectionPathManager
from src.const.error import ERR_UNEXPECTED
from src.core.response.queue_collection.DefaultQueuedCollectionResponseQueueManager import \
    DefaultQueuedCollectionResponseQueueManager
from src.core.response.queue_collection.FastModeQueuedCollectionResponseQueueManager import \
    FastModeQueuedCollectionResponseQueueManager
from src.core.response.AbortResponse import AbortResponse
from src.core.response.queue_collection.QueuedCollectionStopResponse import QueuedCollectionStopResponse
from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class QueuedCollectionResponse(AbstractResponse):
    ids_counter = 0

    def __init__(self, kernel, collection: list):
        super().__init__(kernel)
        self.collection = collection
        self.step_position: int = 0
        self.has_next_step = False
        self.kernel.tmp['last_created_queued_collection'] = self
        self.path_manager: QueuedCollectionPathManager = None

        manager_class = FastModeQueuedCollectionResponseQueueManager \
            if self.kernel.fast_mode \
            else DefaultQueuedCollectionResponseQueueManager
        self.queue_manager = manager_class(self)

        # For debug purpose
        self.id = QueuedCollectionResponse.ids_counter
        QueuedCollectionResponse.ids_counter += 1

    def find_parent_response_collection(self) -> 'None|AbstractResponse':
        current = self
        while current is not None:
            current = current.parent
            if isinstance(current, QueuedCollectionResponse):
                return current

        return None

    def build_step_path(self) -> str:
        return '.'.join(map(str, self.request.steps))

    def render_content(self,
                       request: CommandRequest,
                       render_mode: str = KERNEL_RENDER_MODE_CLI,
                       args: dict = {}) -> AbstractResponse:

        # Share path manager across root request and all involved collections
        root_request = request.get_root_parent()
        if 'queue_collection_path_manager' not in root_request.storage:
            root_request.storage['queue_collection_path_manager'] = QueuedCollectionPathManager(root_request)

        self.path_manager: QueuedCollectionPathManager = root_request.storage['queue_collection_path_manager']
        self.path_manager.set_current_request(request)
        self.path_manager.set_current_response(self)

        # Collection is empty, nothing to do
        if not len(self.collection):
            return self.queue_manager.render_content_complete()

        if self.parent:
            self.step_position = self.find_parent_response_collection().step_position + 1

        # There is a deeper level.
        if self.path_manager.has_child_queue():
            # Append a new step level,
            # set to None to postpone processing
            request.steps.append(None)

        step_index = request.steps[self.step_position]
        self.kernel.io.log(f'Step path : ' + str(self.build_step_path()))
        self.kernel.io.log(f'Step position : ' + str(self.step_position))
        self.kernel.io.log(f'Step index : ' + str(step_index))

        # First time, do not execute, wait next iteration
        if step_index is None:
            self.queue_manager.enqueue_next_step_by_index(0)

            return self.queue_manager.render_content_complete()

        # Prepare args
        render_args = {
            'previous': self.queue_manager.get_previous_value()
        } if step_index > 0 else {}

        # Transform item in a response object.
        wrap = self.request.resolver.wrap_response(self.collection[step_index])
        response = wrap.render(
            request=self.request,
            args=render_args,
            render_mode=render_mode
        )

        first_response_item = None
        if len(response.output_bag) >= 1:
            first_response_item = response.output_bag[0]

        # If first item is of type "response"
        # the base response is probably a function
        # which have been executed and returning a new response
        if isinstance(first_response_item, AbstractResponse):
            response = first_response_item

        # Support simple abort response, with is an alias of a stop response.
        if isinstance(response, AbortResponse):
            response = QueuedCollectionStopResponse(self.kernel, response.reason)

        self.output_bag.append(response)

        # Response can have two different states according the way they have been returned :
        # - When a function return a response class, it has not been rendered
        # - When a function runs a sub command request, it has already been rendered
        if isinstance(response, AbstractResponse) and not response.rendered:
            response.render(
                request,
                render_mode,
                render_args
            )

        # Response asks to stop all process
        if isinstance(response, QueuedCollectionStopResponse):
            # Mark having next step to block enqueuing
            self.has_next_step = True

            return self.queue_manager.render_content_complete()

        if isinstance(response, QueuedCollectionResponse):
            if response.has_next_step:
                self.has_next_step = response.has_next_step
                return self.queue_manager.render_content_complete()
        # If this is not a QueuedCollectionResponse,
        # no new QueuedCollectionResponse should have been created
        # during the rendering process.
        elif self.kernel.tmp['last_created_queued_collection'] != self:
            self.kernel.io.error(ERR_UNEXPECTED, {
                'error': 'When using a nested "QueuedCollectionResponse" it should be returned by its container '
                         'function',
            })

        self.queue_manager.enqueue_next_step_if_exists(step_index, response)

        return self.queue_manager.render_content_complete()
