from typing import cast

from addons.app.typing.webhook import WebhookListenerRoutesMap

from addons.app.command.webhook.exec import app__webhook__exec
from addons.app.command.webhook.status import app__webhook__status
from addons.app.command.webhook.status_process import app__webhook__status_process

WEBHOOK_LISTENER_ROUTES_MAP = cast(WebhookListenerRoutesMap, {
    "exec": {
        "is_async": True,
        "pattern": r"^/webhook/([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-\/]+)$",
        "script_command": app__webhook__exec,
    },
    "status": {
        "is_async": False,
        "pattern": r"^/status$",
        "script_command": app__webhook__status,
    },
    "status_process": {
        "is_async": False,
        "pattern": r"^/status/process/([0-9\-]+)$",
        "script_command": app__webhook__status_process,
    },
})
