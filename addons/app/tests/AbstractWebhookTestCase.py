import json
import os
import shutil
import time
from http.client import HTTPConnection, HTTPResponse
from typing import Optional, Tuple, cast

from addons.app.command.webhook.listen import app__webhook__listen
from addons.app.const.app import APP_DIR_APP_DATA
from addons.app.helper.test import DEFAULT_APP_TEST_NAME
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.types import JsonContent, StringKeysDict


class AbstractWebhookTestCase(AbstractAppTestCase):
    def start_webhook_listener(self, port: int = 6543) -> int:
        self.kernel.run_function(
            app__webhook__listen, {"port": port, "asynchronous": True, "force": True}
        )

        time.sleep(2)

        return port

    def request_listener(
        self, path: str, port: int = 6543, check_code: None | int = 200, wait: int = 0
    ) -> HTTPResponse:
        domain = f"localhost:{port}"

        self.log(f"GET to {domain}{path}")
        conn = HTTPConnection(domain)
        conn.request("GET", path)
        response = conn.getresponse()

        if response.status != 200:
            self.kernel.io.log("STATUS: " + str(response.status))
            error_response_content = response.read()

            try:
                error_data: Optional[JsonContent] = json.loads(error_response_content)
                if "stderr" in error_data:
                    self.kernel.io.log(error_data["stderr"])
            except:
                pass

            self.kernel.io.log(error_response_content)

            if path != "/status":
                self.log("Error : trying to fetch process error info...")

                try:
                    error_process_data = self.parse_response(
                        self.request_listener("/status")
                    )
                    self.kernel.io.log(error_process_data)
                except:
                    pass

        if check_code:
            self.assertEqual(response.status, check_code)

        if wait:
            self.log(f"Wait webhook execution {path}")
            time.sleep(wait)

        return response

    def parse_response(self, response: HTTPResponse) -> JsonContent:
        content = response.read()
        self.kernel.io.log("PARSING : " + str(content))

        data = json.loads(content)
        self.assertTrue(isinstance(data, dict))

        return cast(JsonContent, data)

    def copy_command_dir(self, app_dir: str, sub_dir: str) -> None:
        script_dir = os.path.join(
            app_dir,
            APP_DIR_APP_DATA,
            sub_dir,
        )

        shutil.rmtree(script_dir)

        shutil.copytree(
            os.path.join(
                self.get_app_resources_path(),
                "5.0.0",
                APP_DIR_APP_DATA,
                sub_dir,
            ),
            script_dir,
        )

    def create_and_start_test_app_webhook(self) -> Tuple[str, str]:
        app_dir = self.create_and_start_test_app(
            DEFAULT_APP_TEST_NAME + "-webhook", services=["php"]
        )

        self.copy_command_dir(app_dir, "command")
        self.copy_command_dir(app_dir, "script")

        return app_dir, os.path.basename(os.path.dirname(app_dir))
