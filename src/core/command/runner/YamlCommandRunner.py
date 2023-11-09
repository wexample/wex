import click
from click import Command

from src.helper.yaml import yaml_load
from src.const.error import ERR_UNEXPECTED
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.CommandRequest import CommandRequest
from src.decorator.command import command


class YamlCommandRunner(AbstractCommandRunner):
    def __init__(self, kernel):
        super().__init__(kernel)

    def set_request(self, request: CommandRequest):
        super().set_request(request=request)

        self.content = yaml_load(self.request.path)

        if not self.content:
            self.kernel.io.error(ERR_UNEXPECTED, {
                'error': f'Unable to load yaml script file content :  {self.request.path}',
            })

    def convert_args_dict_to_list(self, args: dict) -> list:
        pass

    def get_request_function(self, path: str, parts) -> Command:
        pass

    def get_params(self) -> list:
        pass

    def get_command_type(self):
        return self.content['type']

    def get_attr(self, name: str, default=None) -> bool:
        pass

    def has_attr(self, name: str) -> bool:
        pass

    @staticmethod
    def click_function_handler(*args, **kwargs):
        pass

    def run(self):

        click_function = command(help=self.content['help'])(self.click_function_handler)

        if 'options' in self.content:
            options = self.content['options']

            for option in options:
                click_function = click.option(
                    option['name'],
                    option['short'],
                    is_flag='is_flag' in option and option['is_flag'],
                    required=option['required'],
                    help=option['help']
                )(click_function)

        return self.run_click_function(
            click_function
        )
