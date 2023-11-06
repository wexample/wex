from __future__ import annotations

from src.core.response.queue_manager.DefaultQueuedCollectionResponseQueueManager import \
    DefaultQueuedCollectionResponseQueueManager
from src.core.response.queue_manager.FastModeQueuedCollectionResponseQueueManager import \
    FastModeQueuedCollectionResponseQueueManager
from src.core.response.AbortResponse import AbortResponse
from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse
from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_CLI, VERBOSITY_LEVEL_MAXIMUM
from src.core.response.AbstractResponse import AbstractResponse


class QueuedCollectionResponse(AbstractResponse):
    ids_counter = 0

    def __init__(self, kernel, collection: list):
        super().__init__(kernel)
        self.collection = collection
        self.step_position: int = 0
        self.has_next_step = False
        # For debug purpose
        self.id = QueuedCollectionResponse.ids_counter
        QueuedCollectionResponse.ids_counter += 1

        self.kernel.tmp['last_created_queued_collection'] = self

        manager_class = FastModeQueuedCollectionResponseQueueManager \
            if self.kernel.fast_mode \
            else DefaultQueuedCollectionResponseQueueManager
        self.queue_manager = manager_class(self)

    def find_parent_response_collection(self) -> 'None|AbstractResponse':
        current = self
        while current is not None:
            current = current.parent
            if isinstance(current, QueuedCollectionResponse):
                return current

        return None

    def build_step_path(self) -> str:
        return '.'.join(map(str, self.request.steps))

    def log(self, message, detail: any = '__EMPTY__'):
        self.kernel.io.log(
            f'#{str(self.id)} ' +
            str(message) + (' : ' + str(detail) if detail != '__EMPTY__' else ''),
            verbosity=VERBOSITY_LEVEL_MAXIMUM
        )

    def render_content(self,
                       request: CommandRequest,
                       render_mode: str = KERNEL_RENDER_MODE_CLI,
                       args: dict = {}) -> AbstractResponse:
        self.kernel.io.log(
            f'Rendering collection #{self.id} : ' + request.command,
            verbosity=VERBOSITY_LEVEL_MAXIMUM
        )

        self.kernel.io.log_indent_up()

        # Collection is empty, nothing to do
        if not len(self.collection):
            self.log('is empty')
            return self.render_content_complete()

        if self.parent:
            self.step_position = self.find_parent_response_collection().step_position + 1

        # There is a deeper level.
        if self.step_position >= len(request.steps):
            # Append a new step level,
            # set to None to postpone processing
            request.steps.append(None)

        step_index = request.steps[self.step_position]
        self.log(f'step path', self.build_step_path())
        self.log(f'step position', self.step_position)
        self.log(f'step index', step_index)

        # First time, do not execute, wait next iteration
        if step_index is None:
            self.log(f'Launching first post-execution')
            self.queue_manager.enqueue_next_step_by_index(0)

            return self.render_content_complete()

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
            response = ResponseCollectionStopResponse(self.kernel, response.reason)

        self.output_bag.append(response)

        # If response is a collection, it can have two different states
        # according the way they have been returned :
        # - When a function return a response class, it has not been rendered
        # - When a function runs a sub command request, it has already been rendered
        if isinstance(response, AbstractResponse) and not response.rendered:
            response.render(
                request,
                render_mode,
                render_args
            )

        # Response asks to stop all process
        if isinstance(response, ResponseCollectionStopResponse):
            self.log('Collection execution aborted', response)

            # Mark having next step to block enqueuing
            self.has_next_step = True

            return self.render_content_complete()

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

            return self.render_content_complete()

        self.log('Searching for next collection item')
        self.queue_manager.enqueue_next_step_if_exists(step_index, response)

        return self.render_content_complete()

    def render_content_complete(self):
        self.kernel.io.log_indent_down()

        self.queue_manager.render_content_complete()

        return self
