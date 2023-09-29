from src.core.CommandRequest import CommandRequest
from src.helper.args import parse_arg
from src.helper.file import remove_file_if_exists
from src.helper.process import process_post_exec_wex
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    previous_render_output = None

    def __init__(self, kernel, collection: list):
        super().__init__(kernel)
        self.collection = collection
        self.request = None
        self.step_position: int = 0
        self.parent = None
        self.has_post_exec = None

    def render(self,
               request: CommandRequest,
               render_mode: str = KERNEL_RENDER_MODE_CLI,
               args={}):

        self.request = request
        self.parent = self.kernel.current_response
        self.kernel.current_response = self

        if self.parent:
            self.step_position = self.parent.step_position + 1

            if self.step_position >= len(request.steps):
                # Append a new step level,
                # set to None to postpone processing
                request.steps.append(None)

        self.kernel.log_indent += self.step_position

        step_index = request.steps[self.step_position]

        # Collection is empty, nothing to do
        if not len(self.collection):
            return None

        # First time, do not execute, wait next iteration
        if step_index is None:
            self.enqueue_next_step(0)

            return self

        # Transform each item in a response object.
        collection: List[AbstractResponse] = [self.request.resolver.wrap_response(item) for item in self.collection]

        # Prepare args
        render_args = {}
        if step_index > 0:
            if self.kernel.allow_post_exec:
                render_args = {'previous': parse_arg(self.kernel.task_file_load('response'))}
                remove_file_if_exists(self.kernel.task_file_path('response'))
            else:
                render_args = {'previous': self.previous_render_output}

        output = self.previous_render_output = collection[step_index].render(
            request=self.request,
            args=render_args
        )

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

        step_next = step_index + 1
        if step_next < len(collection):
            if self.kernel.allow_post_exec:
                serialized = output.print()
                if serialized is not None:
                    # Store response in a file to allow next step to access it.
                    self.kernel.task_file_write('response', serialized)

            self.enqueue_next_step(step_next)

        self.kernel.log_indent -= self.step_position

        return self

    def enqueue_next_step(self, next_step_index):
        self.request.steps[self.step_position] = next_step_index
        self.has_post_exec = True

        args = self.request.args.copy()
        arg_push(args, 'command-request-step', '.'.join(map(str, self.request.steps)))
        arg_push(args, 'log-indent', self.kernel.log_indent)

        root = self.get_root_parent()

        process_post_exec_wex(
            self.kernel,
            root.request.function,
            args
        )
