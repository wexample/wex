import json

from src.core.response.DictResponse import DictResponse
from src.helper.routing import get_route_info, is_allowed_route
from src.decorator.command import command
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON, KERNEL_RENDER_MODE_TERMINAL
from addons.app.decorator.option_webhook_url import option_webhook_url


@command(help="Return process info based on task id", command_type=COMMAND_TYPE_ADDON)
@option_webhook_url()
def app__webhook__status_process(kernel: Kernel, url: str):
    from addons.app.command.webhook.listen import WEBHOOK_LISTENER_ROUTES_MAP

    if not is_allowed_route(url, WEBHOOK_LISTENER_ROUTES_MAP):
        return None

    route_info = get_route_info(url, WEBHOOK_LISTENER_ROUTES_MAP)
    task_id = route_info['match'][0]

    log_content = kernel.task_file_load(
        'json',
        task_id=task_id,
        delete_after_read=False,
        create_if_missing=False)

    return DictResponse(
        kernel,
        json.loads(log_content) if log_content else {},
        cli_render_mode=KERNEL_RENDER_MODE_TERMINAL)
