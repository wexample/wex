import json
from http.client import HTTPConnection
from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.app.helper.remote import remote_get_environment_ip
from src.const.globals import COMMAND_TYPE_ADDON, WEBHOOK_LISTEN_PORT_DEFAULT
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option(
    "--environment",
    "-e",
    type=str,
    required=True,
    help="Remote environment (dev, prod)",
)
@option("--port", "-p", type=int, required=False, help="Remote webhook listener port")
def app__remote__available(
    manager: "AppAddonManager", app_dir: str, environment: str, port: None | int = None
) -> bool:
    domain_or_ip = remote_get_environment_ip(
        manager, environment, command=app__remote__available
    )

    if not domain_or_ip:
        return False

    port = port or WEBHOOK_LISTEN_PORT_DEFAULT

    try:
        address = f"{domain_or_ip}:{port}"
        manager.log(f"Checking {address}")
        conn = HTTPConnection(f"{domain_or_ip}:{port}")
        conn.request("GET", "/status")
        response = conn.getresponse()
        data = json.loads(response.read())

        return bool(data["response"]["process"]["running"])
    except:
        return False
