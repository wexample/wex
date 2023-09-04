import inspect

from src.helper.string import to_kebab_case
from src.helper.process import process_post_exec_wex
from src.const.error import ERR_UNEXPECTED
from src.const.globals import KERNEL_RENDER_MODE_CLI
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

    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        request = self.kernel.current_request
        step_argument_name = 'response_collection_step'
        step_option_name = to_kebab_case(step_argument_name)

        if not hasattr(request.function.callback, 'response_collection'):
            self.error(f'but has no @response_collection decorator')

        sig = inspect.signature(request.function.callback)
        if step_argument_name not in sig.parameters:
            param = sig.parameters[step_argument_name]
            if param.annotation == bool:
                self.error(f'but has no response_collection_step:bool function argument')

        # Wrap responses
        collection = []
        for item in self.collection:
            collection.append(request.resolver.wrap_response(item))

        step = int(request.args_dict[step_option_name]) if step_option_name in request.args_dict else None
        args_dict = request.args_dict.copy()

        # First time
        if step is None:
            args_dict[step_option_name] = 0
            process_post_exec_wex(self.kernel, request.function, args_dict)
            # Do not render, wait next iteration.
            return None
        # This is a valid execution step number.
        elif 0 <= step < len(collection):
            output = collection[step].render()
            step_next = step + 1

            if step_next <= len(collection):
                # Store response in a file to allow next step to access it.
                self.kernel.task_file_write(
                    'response',
                    str(output)
                )

                args_dict[step_option_name] = step_next
                process_post_exec_wex(self.kernel, request.function, args_dict)

            return output
