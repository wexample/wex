from typing import Callable, TYPE_CHECKING

from src.core.command.ScriptCommand import ScriptCommand
from src.core.FunctionProperty import FunctionProperty
from addons.app.decorator.app_dir_option import app_dir_option

if TYPE_CHECKING:
    from src.const.types import Args, Kwargs


class AppCommand(ScriptCommand):
    def __init__(self,
                 function: Callable,
                 command_type: str,
                 decorator_args: 'Args',
                 decorator_kwargs: 'Kwargs') -> None:
        # Get and pop interesting args
        dir_required = decorator_kwargs.pop('dir_required', True)
        should_run = decorator_kwargs.pop('should_run', False)

        super().__init__(
            function,
            command_type,
            decorator_args,
            decorator_kwargs,
        )

        # Do not provide app_dir to function
        FunctionProperty(
            script_command=self,
            property_name='app_dir_required',
            property_value=dir_required)

        self.function = app_dir_option(required=dir_required)(self.function)

        self.function = app_dir_option(required=dir_required)(self.function)

        # Do not check if app is running
        FunctionProperty(
            script_command=self,
            property_name='app_should_run',
            property_value=should_run)

        # Say that the command is available ony in app context
        self.function.app_command = True
