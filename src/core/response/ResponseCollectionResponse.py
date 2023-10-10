from __future__ import annotations

from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse
from src.helper.args import arg_push
from src.core.CommandRequest import CommandRequest
from src.helper.args import parse_arg
from src.helper.file import remove_file_if_exists
from src.helper.process import process_post_exec_wex
from src.const.globals import KERNEL_RENDER_MODE_CLI, VERBOSITY_LEVEL_MAXIMUM
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    ids_counter = 0

    def __init__(self, kernel, collection: list):
        super().__init__(kernel)
        self.collection = collection
        self.step_position: int = 0
        self.has_next_step = False
        # For debug purpose
        self.id = ResponseCollectionResponse.ids_counter
        ResponseCollectionResponse.ids_counter += 1

    def find_parent_response_collection(self) -> 'None|AbstractResponse':
        current = self
        while current is not None:
            current = current.parent
            if isinstance(current, ResponseCollectionResponse):
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
            f'Rendering collection #{self.id}',
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
            self.enqueue_next_step_by_index(0)

            return self.render_content_complete()

        # Prepare args
        render_args = {}
        if step_index > 0:
            has_previous = None
            previous = None
            if self.kernel.fast_mode:
                if self.kernel.previous_response:
                    has_previous = True
                    # Serialize previous data to keep consistency with non-fast mode.
                    previous = self.kernel.previous_response.print(False)
            else:
                has_previous = True
                previous = self.kernel.task_file_load('response')

            if has_previous:
                render_args = {'previous': parse_arg(previous)}

        # Transform item in a response object.
        wrap = self.request.resolver.wrap_response(self.collection[step_index])
        response = wrap.render(
            request=self.request,
            args=render_args
        )

        first_response_item = None
        if len(response.output_bag) >= 1:
            first_response_item = response.output_bag[0]

        if isinstance(first_response_item, ResponseCollectionStopResponse):
            self.log('Collection execution aborted', response)
            return self

        self.log('Response type', response)
        self.log('First response item', first_response_item)

        # Handle nested collection response
        if isinstance(first_response_item, AbstractResponse):
            self.log('First item is a collection')
            self.log('Collection rendered', first_response_item.rendered)

            # Collection has not been rendered :
            # - When a function return a raw collection class, it has not been rendered
            # - When a function runs a sub command request, it has already been rendered
            if not first_response_item.rendered:
                first_response_item.render(
                    request,
                    render_mode,
                    render_args
                )

            self.output_bag += first_response_item.output_bag

            if isinstance(first_response_item, ResponseCollectionResponse):
                self.has_next_step = first_response_item.has_next_step

                # The response has enqueued a post-exec request
                if not first_response_item.has_next_step:
                    self.enqueue_next_step(step_index, response)

            return self.render_content_complete()
        else:
            self.output_bag.append(response)

        self.enqueue_next_step(step_index, response)

        return self.render_content_complete()

    def render_content_complete(self):
        self.kernel.previous_response = self
        self.kernel.io.log_indent_down()

        if self.kernel.fast_mode:
            if self.parent:
                self.parent.has_next_step = self.has_next_step
            else:
                while self.has_next_step:
                    self.has_next_step = False
                    self.kernel.previous_response = self
                    self.kernel.current_response = None

                    args = self.request.args.copy()

                    response = self.kernel.run_function(
                        self.request.function,
                        args
                    )

                    self.output_bag += response.output_bag
            return self

        return self

    def enqueue_next_step(self, current_step_index, response):
        # Now that every render() has ran,
        # we can cleanup the temporary storage.
        remove_file_if_exists(self.kernel.task_file_path('response'))

        self.log('Searching for next collection item')
        next_index = current_step_index + 1
        if next_index < len(self.collection):
            # Storing response to a file is not needed
            # when all scripts are ran in one single thread.
            # The "previous_response" var will be used instead.
            if not self.kernel.fast_mode:
                serialized = response.print()
                if serialized is not None:
                    # Store response in a file to allow next step to access it.
                    self.kernel.task_file_write('response', serialized)

            self.enqueue_next_step_by_index(next_index)

    def enqueue_next_step_by_index(self, next_step_index):
        self.request.steps[self.step_position] = next_step_index
        # Remove obsolete parts.
        del self.request.steps[self.step_position + 1:]
        self.has_next_step = True

        if not self.kernel.fast_mode:
            args = self.request.args.copy()
            arg_push(args, 'command-request-step', self.build_step_path())

            root = self.get_root_parent()

            process_post_exec_wex(
                self.kernel,
                root.request.function,
                args
            )
