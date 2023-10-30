import os
import re

from urllib.parse import urlparse, parse_qs

from addons.core.command.logs.rotate import core__logs__rotate
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from addons.app.command.env.get import app__env__get
from src.helper.command import execute_command


@command(help="Execute a webhook")
@option('--url', '-u', type=str, required=True, help="Argument")
@option('--env', '-e', type=str, required=False, help="Env directory")
def core__webhook__exec(kernel: Kernel, url: str, env: None | str = None) -> bool:
    source_data = {}
    parsed_url = urlparse(url)
    path = parsed_url.path
    pattern = r'^\/webhook/([a-zA-Z_\-]+)/([a-zA-Z_\-]+)$'
    match = re.match(pattern, path)

    kernel.run_function(core__logs__rotate)

    if match:
        app_name, webhook = match.groups()
        query_string = parsed_url.query.replace('+', '%2B')
        query_string_data = parse_qs(query_string)
        has_error = False

        # Get all query parameters
        args = []

        for key, value in query_string_data.items():
            # Prevent risky data.
            if re.search(r'[^a-zA-Z0-9_\-]', key):
                has_error = True
                source_data['invalid_key'] = key

            if re.search(r'[^a-zA-Z0-9_\-\\.~\\+]', value[0]):
                has_error = True
                source_data['invalid_value'] = value[0]

            args.append(f'-{key}')
            # Use only the first value for each key
            args.append(value[0])

        if not has_error:
            env = env or kernel.run_function(app__env__get, {
                'app-dir': kernel.get_path('root')
            }).first()
            working_directory = f"/var/www/{env}/{app_name}"
            source_data['working_directory'] = working_directory
            hook_file = f".wex/webhook/{webhook}.sh"

            if os.path.isdir(working_directory):
                if os.path.isfile(os.path.join(working_directory, hook_file)):
                    # Add the arguments to the command
                    command = ['bash', hook_file] + args

                    kernel.logger.append_event({
                        'url': url,
                        'command': command,
                        'source_data': source_data,
                        'success': True
                    })

                    execute_command(kernel, command, working_directory)
                    return True

                source_data['missing_file'] = hook_file
            else:
                source_data['missing_workdir'] = working_directory

    kernel.logger.append_event({
        'url': url,
        'command': [],
        'source_data': source_data,
        'success': False
    })

    return False
