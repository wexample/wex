import os
import subprocess
from urllib.parse import urlparse, parse_qs
import re
import datetime
import json

from src.core.Kernel import Kernel


class WebhookHandler(Kernel):
    history_days_keep_limit = 30

    def __init__(self, entrypoint_path):
        super().__init__(entrypoint_path)

        # Create logs folder.
        self.path['webhook'] = os.path.join(self.path['tmp'], 'webhook')
        self.path['webhook_log'] = os.path.join(self.path['webhook'], 'log')
        self.path['webhook_history'] = os.path.join(self.path['webhook'], 'history.json')
        os.makedirs(self.path['webhook_log'], exist_ok=True)

        self.cleanup_logs()
        self.cleanup_history()

    def cleanup_logs(self):
        today = datetime.date.today()

        for filename in os.listdir(self.path['webhook_log']):
            date_str = filename.split('-')[0:3]
            date_str = '-'.join(date_str)
            file_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

            if (today - file_date).days > self.history_days_keep_limit:
                os.remove(os.path.join(self.path['webhook_log'], filename))

    def cleanup_history(self):
        with open(self.path['webhook_history'], 'r') as f:
            history = json.load(f)

        current_date = datetime.datetime.now()

        filtered_history = [entry for entry in history if (
                current_date - datetime.datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S.%f')
        ).days <= self.history_days_keep_limit]

        with open(self.path['webhook_history'], 'w') as f:
            json.dump(filtered_history, f, indent=4)

    def execute_command(self, command, working_directory):
        date_now = datetime.date.today()
        date_formatted = date_now.strftime("%Y-%m-%d")

        # Create a log file with the timestamp in its name
        log_file = os.path.join(self.path['webhook_log'], f"{date_formatted}-{self.process_id}.log")

        with open(log_file, 'w') as file:
            subprocess.Popen(command, cwd=working_directory, stdout=file, stderr=subprocess.STDOUT)

    def add_to_history(self, url, command):
        command_info = {
            'url': url,
            'command': command,
            'date': str(datetime.datetime.now()),
            'process_id': self.process_id,
        }

        if os.path.exists(self.path['webhook_history']):
            try:
                with open(self.path['webhook_history'], 'r') as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                history = []
        else:
            history = []

        history.append(command_info)

        with open(self.path['webhook_history'], 'w') as f:
            json.dump(history, f, indent=4)

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

                self.add_to_history(url, command)

                self.execute_command(command, working_directory)
                return True
            else:
                return False
