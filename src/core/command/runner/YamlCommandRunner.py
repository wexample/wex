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

    def run(self):
        def test_func():
            pass

        click_function = command(help=self.content['help'])(test_func)

        return self.run_click_function(
            click_function
        )