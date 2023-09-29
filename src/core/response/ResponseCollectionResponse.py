from __future__ import annotations

import random
from typing import List

from src.helper.args import arg_push, parse_arg
from src.core.CommandRequest import CommandRequest
from src.helper.args import parse_arg
from src.helper.file import remove_file_if_exists
from src.helper.process import process_post_exec_wex
from src.const.globals import KERNEL_RENDER_MODE_CLI, VERBOSITY_LEVEL_MAXIMUM
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    previous_render_response = None

    def __init__(self, kernel, collection: list):
        super().__init__(kernel)
        self.collection = collection
        self.step_position: int = 0
        self.has_post_exec = None
        # For debug purpose
        self.id = random.random()

    def build_step_path(self) -> str:
        return '.'.join(map(str, self.request.steps))

    def log(self, message, detail='__EMPTY__'):
        self.kernel.log(
            str(message) + (' : ' + str(detail) if detail != '__EMPTY__' else ''),
            verbosity=VERBOSITY_LEVEL_MAXIMUM
        )

    def render_content(self,
                       request: CommandRequest,
                       render_mode: str = KERNEL_RENDER_MODE_CLI,
                       args: dict = {}) -> AbstractResponse:
        self.kernel.log(
            f'Rendering collection #{self.id}',
            verbosity=VERBOSITY_LEVEL_MAXIMUM
        )

        self.kernel.log_indent_up()

        if self.parent:
            self.step_position = self.parent.step_position + 1

            if self.step_position >= len(request.steps):
                # Append a new step level,
                # set to None to postpone processing
                request.steps.append(None)

        self.kernel.log_indent += self.step_position

        step_index = request.steps[self.step_position]
        self.log(f'step position', self.step_position)
        self.log(f'step path', self.build_step_path())

        # First time, do not execute, wait next iteration
        if step_index is None:
            self.log(f'Launching first post-execution')
            self.enqueue_next_step(0)

            return self.render_content_complete()

        # Transform each item in a response object.
        collection: List[AbstractResponse] = [self.request.resolver.wrap_response(item) for item in self.collection]

        # Prepare args
        render_args = {}
        if step_index > 0:
            if self.kernel.allow_post_exec:
                render_args = {'previous': parse_arg(self.kernel.task_file_load('response'))}
                remove_file_if_exists(self.kernel.task_file_path('response'))
            else:
                render_args = {'previous': self.previous_render_response.print()}

        # Handle nested collection response
        if isinstance(output, ResponseCollectionResponse):
            self.output_bag += output.output_bag

            # The result is a collection which have enqueued something
            # stop now, until the sub collection is not proceeded
            if output.has_post_exec:
                return output
            else:
                return output.render(
                    request,
                    render_mode,
                    args
                )
        else:
            self.output_bag.append(output)
            self.output_bag.append(response)

        next_index = step_index + 1
        if next_index < len(self.collection):
            if self.kernel.allow_post_exec:
                serialized = response.print()
                if serialized is not None:
                    # Store response in a file to allow next step to access it.
                    self.kernel.task_file_write('response', serialized)

            self.enqueue_next_step(next_index)

        return self.render_content_complete()

    def render_content_complete(self):
        self.kernel.log_indent_down()

        return self

    def enqueue_next_step(self, next_step_index):
        self.request.steps[self.step_position] = next_step_index
        self.has_post_exec = True

        args = self.request.args.copy()
        arg_push(args, 'command-request-step', self.build_step_path())
        # Log level should be at the same level as
        # before current execution
        arg_push(args, 'log-indent', self.kernel.log_indent - 1)

        root = self.get_root_parent()

        process_post_exec_wex(
            self.kernel,
            root.request.function,
            args
        )
