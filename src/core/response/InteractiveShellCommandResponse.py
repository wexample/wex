from src.helper.command import command_to_string, execute_command
from src.core.CommandRequest import CommandRequest
from src.helper.process import process_post_exec
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class InteractiveShellCommandResponse(AbstractResponse):
    def __init__(self, kernel, shell_command: list, ignore_error: bool = False):
        super().__init__(kernel)

        self.shell_command: list = shell_command
        self.interactive_data = True
        self.ignore_error = ignore_error

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> AbstractResponse:

        if self.ignore_error:
            self.shell_command += [
                '||',
                'true'
            ]

        if self.kernel.fast_mode:
            # When using fast mode, we need to preserve consistency between shell executions.
            # Ex : ['echo', '"OK"'] should return OK without quotes.
            # As we don't use shlex to wrap arguments,
            # we need to enable shell=True here.

            success, content = execute_command(
                self.kernel,
                command_to_string(self.shell_command),
                shell=True
            )

            self.success = success

            # Output data as it was printed in a shell.
            self.output_bag.append('\n'.join(content))

        # Do not add to render bag, but append only once.
        elif not self.rendered:
            process_post_exec(
                self.kernel,
                self.shell_command
            )

        return self
