from src.helper.args import parse_arg
from src.helper.file import remove_file_if_exists
from src.helper.process import process_post_exec_wex
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    def __init__(self, kernel, collection: list):
        super().__init__(kernel)
        self.collection = collection

    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI, args={}) -> str | int | bool | None:
        request = self.kernel.current_request

        # Convert step to a list of integers
        step_split = list(map(int, request.step.split('.'))) if request.step else [None]

        return self._render(step_split, 0)

    def _render(self, step_list, step_position: int | None, output_bag: list = None):
        output_bag = output_bag if output_bag is not None else []
        request = self.kernel.current_request
        current_step = step_list[step_position]

        # First time, do not execute, wait next iteration.
        if current_step is None:
            self.enqueue_next_step(step_list, step_position, 0, output_bag)
            return None if self.kernel.allow_post_exec else output_bag

        # Wrap responses
        collection = [request.resolver.wrap_response(item) for item in self.collection]

        render_args = {}
        if current_step > 0:
            render_args = {'previous': parse_arg(self.kernel.task_file_load('response'))}
            remove_file_if_exists(self.kernel.task_file_path('response'))

        output = collection[current_step].render(args=render_args)
        output_bag.append(output)

        # Handle nested collection response
        if isinstance(output, ResponseCollectionResponse):
            step_position += 1
            step_list += [None] * (step_position + 1 - len(step_list))
            return output._render(step_list, step_position, output_bag) if self.kernel.allow_post_exec else output_bag

        step_next = current_step + 1

        if step_next < len(collection):
            # Store response in a file to allow next step to access it.
            self.kernel.task_file_write('response', str(output))
            self.enqueue_next_step(step_list, step_position, step_next, output_bag)

        return output if self.kernel.allow_post_exec else output_bag

    def enqueue_next_step(self, step_list, step_position, step_next, output_bag: list):
        step_list[step_position] = step_next

        if self.kernel.allow_post_exec:
            args_dict = self.kernel.current_request.args_dict.copy()
            args_dict['command-request-step'] = '.'.join(map(str, step_list))
            process_post_exec_wex(self.kernel, self.kernel.current_request.function, args_dict)
        else:
            # Run now.
            self._render(step_list, step_position, output_bag)
