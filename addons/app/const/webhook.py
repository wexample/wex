from typing import cast

from addons.app.command.webhook.exec import app__webhook__exec
from addons.app.command.webhook.status import app__webhook__status
from addons.app.command.webhook.status_process import app__webhook__status_process
from addons.app.typing.webhook import WebhookListenerRoutesMap

WEBHOOK_LISTENER_ROUTES_MAP = cast(
    WebhookListenerRoutesMap,
    {
        "exec": {
            "async": True,
            "pattern": r"^/webhook/([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-\/]+)$",
            "function": app__webhook__exec,
        },
        "status": {
            "async": False,
            "pattern": r"^/status$",
            "function": app__webhook__status,
        },
        "status_process": {
            "async": False,
            "pattern": r"^/status/process/([0-9\-]+)$",
            "function": app__webhook__status_process,
        },
    },
)
