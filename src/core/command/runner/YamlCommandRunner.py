import click
from click import Command

from src.helper.yaml import yaml_load
from src.const.error import ERR_UNEXPECTED
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.CommandRequest import CommandRequest
from src.decorator.command import command
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse

COMMAND_TYPE_BASH = 'bash'
COMMAND_TYPE_BASH_FILE = 'bash-file'
COMMAND_TYPE_PYTHON = 'python'
COMMAND_TYPE_PYTHON_FILE = 'python-file'


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
        def _click_function_handler(*args, **kwargs):
            # manager: AppAddonManager = kernel.addons['app']
            # script_config = manager.load_script(name)
            #
            # if (not script_config
            #         or (webhook and ('webhook' not in script_config or not script_config['webhook']))):
            #     return None

            commands_collection = []
            # counter = 0

            # options = dotenv_values(
            #     os.path.join(
            #         manager.app_dir,
            #         APP_FILEPATH_REL_DOCKER_ENV
            #     )
            # )

            # Iterate through each command in the configuration
            for script in self.content.get('scripts', []):
                if isinstance(script, str):
                    script = {
                        'script': script,
                        'title': script,
                        'type': COMMAND_TYPE_BASH
                    }

                self.kernel.io.log(script['title'])

                for key in kwargs:
                    script['script'] = script['script'].replace('$' + key.upper(), kwargs[key])

                script_part_type = script.get('type', COMMAND_TYPE_BASH)
                command = None
            #     counter += 1
            #
            #     if 'container_name' in script:
            #         script['app_should_run'] = True
            #
            #     if 'app_should_run' in script:
            #         if not kernel.run_function(
            #                 app__app__started,
            #                 {
            #                     'app-dir': app_dir,
            #                 }
            #         ).first():
            #             kernel.io.error(ERR_APP_SHOULD_RUN, {
            #                 'command': script['title'],
            #                 'dir': app_dir,
            #             })
            #
            #             return
            #
                if script_part_type == COMMAND_TYPE_BASH:
                    command = script.get('script', '')
            #     elif script_part_type == COMMAND_TYPE_BASH_FILE:
            #         # File is required in this case.
            #         if 'file' in script_part_type:
            #             command = [
            #                 'bash',
            #                 os.path.join(
            #                     manager.app_dir,
            #                     script['file']
            #                 )
            #             ]
            #     elif script_part_type == COMMAND_TYPE_PYTHON:
            #         if 'script' in script:
            #             escaped_script = script['script'].replace('"', r'\"')
            #
            #             command = [
            #                 'python3',
            #                 '-c',
            #                 f'"{escaped_script}"'
            #             ]
            #     elif script_part_type == COMMAND_TYPE_PYTHON_FILE:
            #         # File is required in this case.
            #         if 'file' in script_part_type:
            #             command = [
            #                 'python3',
            #                 os.path.join(
            #                     manager.app_dir,
            #                     script['file']
            #                 )
            #             ]
            #
                if command:
                    if 'container_name' in script:
                        pass
            #             commands_collection.append(
            #                 _app__script__exec__create_callback(
            #                     kernel, app_dir, command
            #                 )
            #             )
                    else:
                        commands_collection.append(
                            InteractiveShellCommandResponse(self.kernel, command)
                        )

            return QueuedCollectionResponse(self.kernel, commands_collection)

        click_function = command(help=self.content['help'])(_click_function_handler)

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

# def _app__script__exec__create_callback(
#         kernel,
#         app_dir,
#         command):
#     def _callback(previous):
#         return kernel.run_function(
#             app__app__exec,
#             {
#                 'app-dir': app_dir,
#                 'command': command
#             }
#         )
#
#     return _callback