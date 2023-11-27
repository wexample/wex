import json
from http.client import HTTPConnection
from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
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
):
    domain = manager.get_config(f"env.{environment}.domain_main")
    if not domain:
        return

    port = port or WEBHOOK_LISTEN_PORT_DEFAULT

    try:
        conn = HTTPConnection(f"{domain}:{port}")
        conn.request("GET", "/status")
        response = conn.getresponse()
        data = json.loads(response.read())

        return data["response"]["process"]["running"]
    except:
        return False
