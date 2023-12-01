from typing import TYPE_CHECKING, Dict, Optional, TypedDict, cast

from addons.app.decorator.option_webhook_listener import option_webhook_listener
from src.const.globals import COMMAND_TYPE_ADDON, KERNEL_RENDER_MODE_TERMINAL
from src.const.types import StringKeysDict
from src.core.Logger import LoggerLogData
from src.core.response.DictResponse import DictResponse
from src.decorator.command import command
from src.helper.routing import routing_get_route_info, routing_is_allowed_route

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class StatusProcess(TypedDict, total=False):
    task: LoggerLogData
    children: Dict[str, LoggerLogData]


@command(help="Return process info based on task id", command_type=COMMAND_TYPE_ADDON)
@option_webhook_listener(path=True)
def app__webhook__status_process(
    kernel: "Kernel", webhook_path: str
) -> Optional[DictResponse]:
    from addons.app.const.webhook import WEBHOOK_LISTENER_ROUTES_MAP

    if not routing_is_allowed_route(webhook_path, WEBHOOK_LISTENER_ROUTES_MAP):
        return None

    output = StatusProcess()
    route_info = routing_get_route_info(webhook_path, WEBHOOK_LISTENER_ROUTES_MAP)
    if route_info:
        match = route_info["match"]
        task_id = match.group(0)

        if task_id:
            log_content = kernel.logger.load_logs(task_id)

            if log_content:
                output["task"] = log_content
                output["children"] = {}

                for date in log_content["children"]:
                    child_task_id = log_content["children"][date]

                    output["children"][child_task_id] = kernel.logger.load_logs(
                        child_task_id
                    )

    return DictResponse(
        kernel,
        cast(StringKeysDict, output),
        cli_render_mode=KERNEL_RENDER_MODE_TERMINAL,
    )
