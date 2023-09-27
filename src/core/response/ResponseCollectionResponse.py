import inspect

from src.helper.args import parse_arg
from src.helper.file import remove_file_if_exists
from src.helper.string import to_kebab_case
from src.helper.process import process_post_exec_wex
from src.const.error import ERR_UNEXPECTED
from src.const.globals import KERNEL_RENDER_MODE_CLI, KERNEL_RENDER_MODE_COMMAND
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    def __init__(self, kernel, collection: list):
        super().__init__(kernel)

        self.collection = collection

    def error(self, message_end):
        request = self.kernel.current_request

        self.kernel.error(
            ERR_UNEXPECTED,
            {
                'error': f'Command "{request.command}" returns a {str(type(self))} response, {message_end}'
            }
        )

    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI, args={}) -> str | int | bool | None:
        request = self.kernel.current_request

        # Convert step to a list of integers
        step_split = list(map(int, request.step.split('.'))) if request.step is not None else [None]

        return self._render(step_split, 0)

    def _render(self, step_list, step_position: int | None):
        request = self.kernel.current_request
        args_dict = request.args_dict.copy()
        current_step = step_list[step_position]

        # First time
        if current_step is None:
            step_list[step_position] = 0
            args_dict['command-request-step'] = '.'.join(map(str, step_list))
            process_post_exec_wex(self.kernel, request.function, args_dict)
            # Do not render, wait next iteration.
            return None

        # Wrap responses
        collection = []
        for item in self.collection:
            collection.append(request.resolver.wrap_response(item))

        render_args = {}
        if current_step > 0:
            render_args = {
                'previous': parse_arg(
                    self.kernel.task_file_load(
                        'response',
                    )
                )
            }

            remove_file_if_exists(
                self.kernel.task_file_path('response')
            )

        output = collection[current_step].render(
            args=render_args
        )

        # If the output is a sub-collection, append a new level to step
        if isinstance(output, ResponseCollectionResponse):
            step_position += 1

            # Set value at step_position, extending the list with None values if necessary
            step_list.extend([None] * (step_position - len(step_list) + 1)) if step_position >= len(step_list) else None

            return output._render(step_list, step_position)

        step_next = current_step + 1

        if step_next < len(collection):
            step_list[step_position] = step_next
            # Store response in a file to allow next step to access it.
            self.kernel.task_file_write(
                'response',
                str(output)
            )

            args_dict['command-request-step'] = '.'.join(map(str, step_list))
            process_post_exec_wex(self.kernel, request.function, args_dict)

        return output
