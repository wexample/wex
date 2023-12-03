from typing import Dict, Pattern, TypedDict

from src.const.types import StringsList
from src.core.command.ScriptCommand import ScriptCommand


class WebhookRoute(TypedDict):
    command: StringsList
    is_async: bool
    pattern: Pattern[str]
    script_command: ScriptCommand


WebhookListenerRoutesMap = Dict[str, WebhookRoute]
