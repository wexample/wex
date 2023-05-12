import os
import subprocess
from urllib.parse import urlparse, parse_qs
import re
import datetime

from src.core.Kernel import Kernel


class WebhookHandler(Kernel):
    def __init__(self, entrypoint_path):
        super().__init__(entrypoint_path)

        # Create logs folder.
        self.path['webhook_logs'] = os.path.join(self.path['tmp'], 'webhook')
        os.makedirs(self.path['webhook_logs'], exist_ok=True)

    def execute_command(self, command, working_directory):
        # Create a log file with the timestamp in its name
        log_file = os.path.join(self.path['webhook_logs'], f"{self.process_id}.log")

        with open(log_file, 'w') as file:
            subprocess.Popen(command, cwd=working_directory, stdout=file, stderr=subprocess.STDOUT)

    def parse_url_and_execute(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        pattern = r'^\/webhook/([a-zA-Z_\-]+)/([a-zA-Z_\-]+)$'
        match = re.match(pattern, path)

        if match:
            app_name, webhook = match.groups()
            query_string_data = parse_qs(parsed_url.query)

            # Get all query parameters
            args = []
            for key, value in query_string_data.items():
                # Prevent risky data.
                if re.search(r'[^a-zA-Z0-9_\-]', key) or re.search(r'[^a-zA-Z0-9_\-.~]', value[0]):
                    return False

                args.append(key)
                # Use only the first value for each key
                args.append(value[0])

            env = self.get_env()
            working_directory = f"/var/www/{env}/{app_name}"
            hook_file = f".wex/webhook/{webhook}.sh"

            if os.path.isdir(working_directory) and os.path.isfile(os.path.join(working_directory, hook_file)):
                # Add the arguments to the command
                command = ['bash', hook_file] + args
                self.execute_command(command, working_directory)
                return True
            else:
                return False
