from __future__ import annotations

from re import Pattern
from typing import Dict, TypedDict

from src.const.types import StringsList
from src.core.command.ScriptCommand import ScriptCommand


class WebhookRoute(TypedDict):
    command: StringsList
    is_async: bool
    pattern: Pattern[str]
    script_command: ScriptCommand


WebhookListenerRoutesMap = dict[str, WebhookRoute]
