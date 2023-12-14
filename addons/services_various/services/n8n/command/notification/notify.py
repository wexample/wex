from typing import TYPE_CHECKING, Optional

import requests
from requests.auth import HTTPBasicAuth

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="send app notification to service", command_type=COMMAND_TYPE_SERVICE)
@option("--action", "-a", type=str, required=True, help="Action name")
def n8n__notification__notify(
    manager: "AppAddonManager", app_dir: str, service: str, action: str
) -> None:
    protocol = manager.get_config("notification.protocol", "https").get_str()
    domain = manager.get_config("notification.domain").get_str()
    test = manager.get_config("notification.test", False).get_bool()
    webhook_id = manager.get_config("notification.webhook_id").get_str()

    url = f"{protocol}://{domain}/webhook{'-test' if test else ''}/{webhook_id}"

    auth: Optional[HTTPBasicAuth] = None

    if manager.has_config("notification.auth"):
        auth_user = manager.get_config("notification.auth.login").get_str()
        auth_password = manager.get_config("notification.auth.password").get_str()

        auth = HTTPBasicAuth(auth_user, auth_password)

    headers = {"Content-Type": "application/json"}

    data = {"app": manager.get_config("global.name").get_str(), "action": action}

    manager.log(f"Sending notification '{action}' to {url}")

    requests.post(url, json=data, headers=headers, auth=auth)
