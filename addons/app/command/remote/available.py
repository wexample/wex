from src.decorator.option import option
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON, WEBHOOK_LISTEN_PORT_DEFAULT
from addons.app.decorator.app_command import app_command
from addons.app.AppAddonManager import AppAddonManager
from http.client import HTTPConnection
import json


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option('--environment', '-e', type=str, required=True, help="Remote environment (dev, prod)")
@option('--port', '-p', type=int, required=False, help="Remote webhook listener port")
def app__remote__available(kernel: Kernel, app_dir: str, environment: str, port: None | int = None):
    manager: AppAddonManager = kernel.addons['app']

    domain = manager.get_config(f'env.{environment}.domain_main')
    if not domain:
        return

    port = port or WEBHOOK_LISTEN_PORT_DEFAULT

    try:
        conn = HTTPConnection(f'{domain}:{port}')
        conn.request("GET", '/status')
        response = conn.getresponse()
        data = json.loads(response.read())

        return data['response']['process']['running']
    except:
        return False